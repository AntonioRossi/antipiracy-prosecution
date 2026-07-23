"""Acceptance criteria AC-01 … AC-20 (TDD §14) — the live tests behind
schema/acceptance.json. Function names are registered in the criteria
registry; the traceability meta-test (AC-19) closes both directions over
the registry, itself included.
"""

import ast
import base64
import copy
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from html.parser import HTMLParser
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import (acceptance, authority, bundlezip, canon, control_inventory,
                 currentstate, gateway, inputlock, model, profilepolicy,
                 projections, recordprovenance, render_inventory)  # noqa: E402
from lib import render, schema_validate, validate  # noqa: E402
from tests import acceptance_support  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NAV = os.path.dirname(HERE)
ROOT = os.path.dirname(NAV)
DIST = os.path.join(NAV, "dist")
RECORDS = os.path.join(NAV, "records")
EDITIONS = ("na", "af")
TDD = os.path.join(
    ROOT, "AA11393US-claims-navigator_technical-description_DRAFT.md")
ACCEPTANCE_CALLBACK_CONTEXT = None

TECHNICAL_PREVIEW_PROFILE = acceptance_support.TECHNICAL_PREVIEW_PROFILE
VALIDATED_RELEASE_PROFILE = acceptance_support.VALIDATED_RELEASE_PROFILE

_cache = {}


def file_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def file_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def get_model(edition_id):
    if edition_id not in _cache:
        boot = gateway.ContentGateway(ROOT)
        allow = canon.parse_json(boot.read_text(
            "navigator/editions/%s.json" % edition_id))
        gw = gateway.ContentGateway(
            ROOT, allowlist=allow["declaredTransitiveInputs"])
        _cache[edition_id] = model.EditionModel(
            gw, "navigator/editions/%s.json" % edition_id)
    return _cache[edition_id]


def get_html(edition_id, mode="candidate"):
    key = (edition_id, mode)
    if key not in _cache:
        _cache[key] = render.render(get_model(edition_id), mode=mode)
    return _cache[key]


def get_errors(edition_id):
    key = (edition_id, "errors")
    if key not in _cache:
        _cache[key] = validate.validate_edition(get_model(edition_id))
    return _cache[key]


def read_records(kind):
    if not os.path.isdir(RECORDS):
        return []
    planes = canon.parse_json(gateway.ContentGateway(ROOT).read_text(
        "navigator/schema/planes.json"))
    return gateway.VerificationGateway(
        RECORDS, "status", planes).read_all(kind)


def fixture(name):
    with open(os.path.join(HERE, "fixtures", name), encoding="utf-8") as fh:
        return canon.parse_json(fh.read())


def _resolved_schema(schema, root):
    while "$ref" in schema:
        node = root
        for part in schema["$ref"][2:].split("/"):
            node = node[part]
        schema = node
    return schema


def _schema_ship_paths(schema, root, ship_value, path="$"):
    """Derive every path carrying one x-ship value from the live schema."""
    schema = _resolved_schema(schema, root)
    tagged = schema.get("x-ship")
    if tagged is not None:
        return {path} if tagged == ship_value else set()
    paths = set()
    if schema.get("type") == "object":
        for name, child in schema.get("properties", {}).items():
            paths.update(_schema_ship_paths(
                child, root, ship_value, "%s.%s" % (path, name)))
        for pattern, child in schema.get("patternProperties", {}).items():
            paths.update(_schema_ship_paths(
                child, root, ship_value,
                "%s.<%s>" % (path, pattern)))
    elif schema.get("type") == "array":
        paths.update(_schema_ship_paths(
            schema.get("items", {}), root, ship_value, path + "[]"))
    return paths


_NO_SCHEMA_VALUE = object()


def _pattern_example(pattern):
    for candidate in ("c1", "c1u0", "x", "0"):
        if re.fullmatch(pattern, candidate):
            return candidate
    raise AssertionError("no test key satisfies schema pattern %r" % pattern)


def _never_only_instance(schema, root, markers, path="$"):
    """Build a maximal synthetic instance containing every never path.

    Values need not satisfy semantic enums: this instance tests only the
    schema-driven projection. Tagged containers are opaque to that projection.
    """
    schema = _resolved_schema(schema, root)
    tagged = schema.get("x-ship")
    if tagged is not None:
        if tagged != "never":
            return _NO_SCHEMA_VALUE
        marker = "__AC08_NEVER_%03d__" % len(markers)
        markers[path] = marker
        return marker
    if schema.get("type") == "object":
        value = {}
        for name, child_schema in schema.get("properties", {}).items():
            child = _never_only_instance(
                child_schema, root, markers, "%s.%s" % (path, name))
            if child is not _NO_SCHEMA_VALUE:
                value[name] = child
        for pattern, child_schema in schema.get(
                "patternProperties", {}).items():
            name = _pattern_example(pattern)
            child = _never_only_instance(
                child_schema, root, markers,
                "%s.<%s>" % (path, pattern))
            if child is not _NO_SCHEMA_VALUE:
                value[name] = child
        return value if value else _NO_SCHEMA_VALUE
    if schema.get("type") == "array":
        child = _never_only_instance(
            schema.get("items", {}), root, markers, path + "[]")
        return [child] if child is not _NO_SCHEMA_VALUE else _NO_SCHEMA_VALUE
    return _NO_SCHEMA_VALUE


def _ship_axis_leaks(instance, schema, root, path="$"):
    """Return schema paths at which projected data retained x-ship:never."""
    schema = _resolved_schema(schema, root)
    leaks = []
    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        patterns = schema.get("patternProperties", {})
        for name, value in instance.items():
            child_schema = properties.get(name)
            if child_schema is None:
                child_schema = next((candidate for pattern, candidate in
                                     patterns.items()
                                     if re.match(pattern, name)), None)
            if child_schema is None:
                continue
            resolved = _resolved_schema(child_schema, root)
            child_path = "%s.%s" % (path, name)
            if resolved.get("x-ship") == "never":
                leaks.append(child_path)
            elif resolved.get("x-ship") is None:
                leaks.extend(_ship_axis_leaks(
                    value, child_schema, root, child_path))
    elif isinstance(instance, list):
        for index, value in enumerate(instance):
            leaks.extend(_ship_axis_leaks(
                value, schema.get("items", {}), root,
                "%s[%d]" % (path, index)))
    return leaks


class _StaticSectionParser(HTMLParser):
    """Collect visible text, element ids, and attributes by static section."""

    VOID_ELEMENTS = frozenset({
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    })

    def __init__(self, section_ids):
        super().__init__(convert_charrefs=True)
        self.section_ids = set(section_ids)
        self.text = {section_id: [] for section_id in section_ids}
        self.elements = {section_id: [] for section_id in section_ids}
        self.active = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if self.active is None and attributes.get("id") in self.section_ids:
            self.active = attributes["id"]
            self.depth = 1
        elif self.active is not None and tag not in self.VOID_ELEMENTS:
            self.depth += 1
        if self.active is not None:
            self.elements[self.active].append((tag, attributes))
            if tag == "br":
                self.text[self.active].append(" ")

    def handle_startendtag(self, tag, attrs):
        if self.active is not None:
            self.elements[self.active].append((tag, dict(attrs)))

    def handle_endtag(self, unused_tag):
        if self.active is None:
            return
        self.depth -= 1
        if self.depth == 0:
            self.active = None

    def handle_data(self, data):
        if self.active is not None:
            self.text[self.active].append(data)

    def normalized_text(self, section_id):
        return " ".join("".join(self.text[section_id]).split())


def _without_scripts(html):
    return re.sub(
        r"<script\b[^>]*>.*?</script\s*>", "", html,
        flags=re.I | re.S)


def candidate_path(m):
    return os.path.join(DIST, "candidate_" + m.edition["artifactName"])


def run_api_probe_harness(probe_source, policy, scenario):
    """Execute the artifact's real probe bootstrap in a deterministic DOM.

    The failure scenarios deliberately leave a callable API/accessor in
    place while making its hook impossible to install.  An empty attempts
    list is therefore demonstrably untrustworthy unless the installation
    ledger is exact and ready.
    """
    script = r"""
'use strict';
var probeSource = %s;
var policy = %s;
var scenario = %s;
var calls = {push:0, localGet:0, cookieWrite:0};
function noop(){}

global.window = global;
Object.defineProperty(global, 'navigator', {
  configurable:true, writable:true, value:{sendBeacon:noop}
});

var historyValue;
if (scenario === 'nonwritable-function') {
  var historyProto = {};
  Object.defineProperty(historyProto, 'pushState', {
    configurable:false, writable:false,
    value:function(){ calls.push += 1; }
  });
  historyValue = Object.create(historyProto);
  historyValue.replaceState = noop;
} else {
  historyValue = {
    pushState:function(){ calls.push += 1; }, replaceState:noop
  };
}
Object.defineProperty(global, 'history', {
  configurable:true, writable:true, value:historyValue
});

Object.defineProperty(global, 'localStorage', {
  configurable:scenario !== 'getter-failure', enumerable:true,
  get:function(){ calls.localGet += 1; return {}; }
});
Object.defineProperty(global, 'sessionStorage', {
  configurable:true, enumerable:true, get:function(){ return {}; }
});

function IDBFactory(){}
IDBFactory.prototype.open = noop;
global.IDBFactory = IDBFactory;
global.indexedDB = new IDBFactory();

function Document(){}
Object.defineProperty(Document.prototype, 'cookie', {
  configurable:scenario !== 'cookie-failure', enumerable:true,
  get:function(){ return ''; },
  set:function(){ calls.cookieWrite += 1; }
});
global.Document = Document;
global.document = new Document();
document.getElementById = function(id){
  if (id !== 'api-probes') throw new Error('unexpected element ' + id);
  return {textContent:JSON.stringify(policy)};
};

var thrown = null;
try { eval(probeSource); }
catch (error) { thrown = String(error && error.message || error); }
var before = window.__apiAttempts ? window.__apiAttempts.slice() : null;
var deltas = {};
function capture(api, action){
  var start = window.__apiAttempts ? window.__apiAttempts.length : 0;
  action();
  deltas[api] = window.__apiAttempts ?
    window.__apiAttempts.slice(start) : null;
}

if (scenario === 'success') {
  capture('navigator.sendBeacon', function(){ navigator.sendBeacon(); });
  capture('history.pushState', function(){ history.pushState(); });
  capture('history.replaceState', function(){ history.replaceState(); });
  capture('window.localStorage', function(){ void window.localStorage; });
  capture('window.sessionStorage', function(){ void window.sessionStorage; });
  capture('indexedDB.open', function(){ window.indexedDB.open(); });
  capture('document.cookie', function(){ document.cookie = 'probe=1'; });
} else if (scenario === 'nonwritable-function') {
  capture('history.pushState', function(){ history.pushState(); });
} else if (scenario === 'getter-failure') {
  capture('window.localStorage', function(){ void window.localStorage; });
} else if (scenario === 'cookie-failure') {
  capture('document.cookie', function(){ document.cookie = 'probe=1'; });
}

process.stdout.write(JSON.stringify({
  status:window.__apiProbeStatus, before:before,
  after:window.__apiAttempts ? window.__apiAttempts.slice() : null,
  deltas:deltas, thrown:thrown, calls:calls
}));
""" % (json.dumps(probe_source), json.dumps(policy), json.dumps(scenario))
    completed = subprocess.run(
        ["node", "-e", script], capture_output=True, text=True, timeout=30)
    if completed.returncode != 0:
        raise AssertionError(completed.stderr)
    return json.loads(completed.stdout)


def run_navigation_harness(html, runtime_source=None):
    """Execute the candidate's complete runtime in a deterministic DOM.

    The harness deliberately implements only browser primitives used by the
    artifact.  It does not substitute renderer helpers or import source JS:
    ``runtime_source`` defaults to the final inline script extracted from the
    built candidate bytes.  The override exists solely for the AC-10 mutation
    regression.
    """
    nav_match = re.search(
        r'<script type="application/json" id="nav-data">(.*?)</script>',
        html, re.S)
    probe_match = re.search(
        r'<script type="application/json" id="api-probes">(.*?)</script>',
        html, re.S)
    script_match = re.search(r'<script>(.*?)</script>\s*</body>', html, re.S)
    if not nav_match or not probe_match or not script_match:
        raise AssertionError("candidate runtime scripts are not extractable")
    if runtime_source is None:
        runtime_source = script_match.group(1)

    script = r"""
'use strict';
var runtimeSource = @@RUNTIME@@;
var navText = @@NAVDATA@@;
var probeText = @@PROBES@@;
var fails = [];
var coverage = {
  units:0, phrases:0, pointerActivations:0, reverseActivations:0,
  gateActivations:0, sourceQuotes:0
};
function check(condition, message){ if (!condition) fails.push(message); }
function includes(text, part){ return String(text).indexOf(String(part)) >= 0; }

function ClassList(owner){ this.owner = owner; this.values = []; }
ClassList.prototype._set = function(value){
  this.values = String(value || '').split(/\s+/).filter(Boolean);
};
ClassList.prototype.contains = function(value){
  return this.values.indexOf(value) >= 0;
};
ClassList.prototype.add = function(){
  for (var i = 0; i < arguments.length; i++)
    if (!this.contains(arguments[i])) this.values.push(arguments[i]);
};
ClassList.prototype.remove = function(){
  for (var i = 0; i < arguments.length; i++){
    var at;
    while ((at = this.values.indexOf(arguments[i])) >= 0)
      this.values.splice(at, 1);
  }
};
ClassList.prototype.toggle = function(value){
  if (this.contains(value)){ this.remove(value); return false; }
  this.add(value); return true;
};
ClassList.prototype.toString = function(){ return this.values.join(' '); };

function Element(tag, owner){
  this.tagName = String(tag).toUpperCase();
  this.ownerDocument = owner;
  this.parentNode = null;
  this.children = [];
  this.attributes = {};
  this.dataset = {};
  this.hidden = false;
  this._text = '';
  this._listeners = {};
  this._scrolls = [];
  this.classList = new ClassList(this);
}
Object.defineProperty(Element.prototype, 'className', {
  configurable:true,
  get:function(){ return this.classList.toString(); },
  set:function(value){ this.classList._set(value); }
});
Object.defineProperty(Element.prototype, 'textContent', {
  configurable:true,
  get:function(){
    return this._text + this.children.map(function(child){
      return child.textContent;
    }).join('');
  },
  set:function(value){
    this.children.forEach(function(child){ child.parentNode = null; });
    this.children = [];
    this._text = value == null ? '' : String(value);
  }
});
Element.prototype.appendChild = function(child){
  if (child.parentNode) child.remove();
  child.parentNode = this;
  this.children.push(child);
  return child;
};
Element.prototype.remove = function(){
  if (!this.parentNode) return;
  var at = this.parentNode.children.indexOf(this);
  if (at >= 0) this.parentNode.children.splice(at, 1);
  this.parentNode = null;
};
Element.prototype.setAttribute = function(name, value){
  value = String(value);
  this.attributes[name] = value;
  if (name === 'class') this.className = value;
};
Element.prototype.getAttribute = function(name){
  if (name === 'class') return this.className;
  return Object.prototype.hasOwnProperty.call(this.attributes, name) ?
    this.attributes[name] : null;
};
Element.prototype.addEventListener = function(type, listener){
  (this._listeners[type] || (this._listeners[type] = [])).push(listener);
};
Element.prototype._invoke = function(event){
  (this._listeners[event.type] || []).slice().forEach(function(listener){
    listener.call(this, event);
  }, this);
};
Element.prototype.contains = function(node){
  while (node){ if (node === this) return true; node = node.parentNode; }
  return false;
};
Element.prototype.focus = function(){ this.ownerDocument.activeElement = this; };
Element.prototype.scrollIntoView = function(options){ this._scrolls.push(options); };
Element.prototype._matches = function(selector){
  if (selector.charAt(0) === '.') return this.classList.contains(selector.slice(1));
  return this.tagName.toLowerCase() === selector.toLowerCase();
};
Element.prototype.querySelectorAll = function(selector){
  var found = [];
  function visit(node){
    node.children.forEach(function(child){
      if (child._matches(selector)) found.push(child);
      visit(child);
    });
  }
  visit(this);
  return found;
};
Element.prototype.querySelector = function(selector){
  return this.querySelectorAll(selector)[0] || null;
};
Element.prototype.closest = function(selector){
  var node = this;
  while (node){
    if (node._matches && node._matches(selector)) return node;
    node = node.parentNode;
  }
  return null;
};
Element.prototype.click = function(){
  var event = makeEvent('click', this);
  this._invoke(event);
  if (!event._stopped) this.ownerDocument._invoke(event);
  return event;
};

function makeEvent(type, target){
  return {
    type:type, target:target, key:null, defaultPrevented:false, _stopped:false,
    preventDefault:function(){ this.defaultPrevented = true; },
    stopPropagation:function(){ this._stopped = true; }
  };
}
function Document(){
  this._byId = {};
  this._listeners = {};
  this.activeElement = null;
  this.body = new Element('body', this);
}
Document.prototype.createElement = function(tag){ return new Element(tag, this); };
Document.prototype.register = function(element, id){
  if (id){ element.id = id; this._byId[id] = element; }
  return element;
};
Document.prototype.getElementById = function(id){ return this._byId[id] || null; };
Document.prototype.querySelectorAll = function(selector){
  return this.body.querySelectorAll(selector);
};
Document.prototype.addEventListener = function(type, listener){
  (this._listeners[type] || (this._listeners[type] = [])).push(listener);
};
Document.prototype._invoke = function(event){
  (this._listeners[event.type] || []).slice().forEach(function(listener){
    listener.call(this, event);
  }, this);
};
Document.prototype.keydown = function(key){
  var event = makeEvent('keydown', this.activeElement || this.body);
  event.key = key;
  this._invoke(event);
  return event;
};
Object.defineProperty(Document.prototype, 'cookie', {
  configurable:true, enumerable:true,
  get:function(){ return ''; }, set:function(value){ void value; }
});

function noop(){}
global.window = global;
global.Document = Document;
global.document = new Document();
Object.defineProperty(global, 'navigator', {
  configurable:true, writable:true, value:{sendBeacon:noop}
});
Object.defineProperty(global, 'history', {
  configurable:true, writable:true,
  value:{pushState:noop, replaceState:noop}
});
Object.defineProperty(global, 'localStorage', {
  configurable:true, enumerable:true, get:function(){ return {}; }
});
Object.defineProperty(global, 'sessionStorage', {
  configurable:true, enumerable:true, get:function(){ return {}; }
});
function IDBFactory(){}
IDBFactory.prototype.open = noop;
global.IDBFactory = IDBFactory;
global.indexedDB = new IDBFactory();
global.__selectionText = '';
global.getSelection = function(){
  return {toString:function(){ return global.__selectionText; }};
};
global.matchMedia = function(){ return {matches:false}; };

function add(tag, id, classes, parent){
  var node = document.register(document.createElement(tag), id || null);
  if (classes) node.className = classes;
  (parent || document.body).appendChild(node);
  return node;
}
function addButton(id, classes, parent, data){
  var button = add('button', id, classes, parent);
  Object.keys(data || {}).forEach(function(key){ button.dataset[key] = data[key]; });
  button.type = 'button';
  return button;
}
var navScript = add('script', 'nav-data');
navScript.textContent = navText;
var probeScript = add('script', 'api-probes');
probeScript.textContent = probeText;
var forwardBar = add('div', 'forward-bar', 'navbar');
forwardBar.hidden = true;
var reverseBar = add('div', 'reverse-bar', 'navbar');
reverseBar.hidden = true;
var live = add('div', 'live', 'visually-hidden');
var DATA_INPUT = JSON.parse(navText);
var unitPointers = {};

Object.keys(DATA_INPUT.fragments).forEach(function(fid){
  var unit = add('div', 'u-' + fid, 'unit', document.body);
  addButton('btn-' + fid, 'unit-btn', unit, {frag:fid});
  var pointer = add('span', null, 'pointer-surface', unit);
  pointer.dataset.frag = fid;
  unitPointers[fid] = pointer;
  (DATA_INPUT.fragments[fid].phrases || []).forEach(function(phrase){
    addButton('btn-' + phrase.id, 'phrase-btn', unit, {frag:phrase.id});
  });
});
Object.keys(DATA_INPUT.anchors).forEach(function(block){
  if (!document.getElementById(block)) add('div', block, 'dblock');
});
Object.keys(DATA_INPUT.reverse).forEach(function(block){
  var target = document.getElementById(block) || add('div', block, 'dblock');
  var badge = addButton('btn-rev-' + block, 'rev-badge', target,
    {block:block});
  badge.textContent = '◂ ' + DATA_INPUT.reverse[block].length;
});
Object.keys(DATA_INPUT.claimGates).forEach(function(claimKey){
  DATA_INPUT.claimGates[claimKey].forEach(function(gate){
    addButton('btn-gate-' + claimKey + '-' + gate.gateId, 'gate-chip',
      document.body, {gate:gate.gateId, claim:claimKey});
  });
});

var runtimeError = null;
try {
  (0, eval)(runtimeSource +
    '\n;globalThis.__navHarnessRuntime = {model:NavModel, data:DATA};');
} catch (error) {
  runtimeError = String(error && error.stack || error);
}
check(runtimeError === null, 'candidate runtime threw: ' + runtimeError);
var exported = global.__navHarnessRuntime || {};
var NavModel = exported.model;
var DATA = exported.data || DATA_INPUT;
check(!!NavModel, 'selection model unavailable');
check((document._listeners.click || []).length > 0,
      'runtime click handler missing');
check((document._listeners.keydown || []).length > 0,
      'runtime keydown handler missing');
check(window.__apiProbeStatus && window.__apiProbeStatus.ready === true,
      'runtime API probes not ready');

function sourceNode(fragmentId){
  return document.getElementById('u-' + fragmentId) ||
    document.getElementById('btn-' + fragmentId);
}
function allEntries(){
  var out = [];
  Object.keys(DATA.fragments).forEach(function(fid){
    out.push({id:fid, kind:'unit'});
    (DATA.fragments[fid].phrases || []).forEach(function(phrase){
      out.push({id:phrase.id, kind:'phrase'});
    });
  });
  return out;
}
function buttonByLabel(root, label){
  return root.querySelectorAll('button').filter(function(button){
    return button.getAttribute('aria-label') === label;
  })[0] || null;
}
function positionText(position, total, label){
  return DATA.strings.ui.position
    .split('{position}').join(String(position))
    .split('{total}').join(String(total))
    .split('{label}').join(String(label));
}
function claimOf(fragmentId){
  return 'c' + parseInt(fragmentId.slice(1), 10);
}
function applicableCaution(info, target){
  return !!(info && (info.caution || (target && target.caution)));
}
function checkPresence(text, info, fragmentId, target, context){
  check(includes(text, DATA.strings.ui.cautionPresent) ===
    applicableCaution(info, target), context + ' caution announcement');
  var gatePresent = (DATA.claimGates[claimOf(fragmentId)] || []).length > 0;
  check(includes(text, DATA.strings.ui.gatePresent) === gatePresent,
        context + ' gate announcement');
}
function checkForwardLive(fragmentId, info, position, context){
  var text = live.textContent;
  check(includes(text, DATA.strings.ui.forwardMode), context + ' live mode');
  check(includes(text, DATA.unitLabels[fragmentId] || fragmentId),
        context + ' live subject');
  var target = null;
  if (info.status === 'mapped'){
    target = info.targets[position];
    var targetName = DATA.anchors[target.block] || target.block;
    check(includes(text, positionText(position + 1, info.targets.length,
      targetName)), context + ' live position/target');
  } else {
    check(includes(text, DATA.strings.ui.noCandidateNotice),
          context + ' live no-candidate notice');
  }
  checkPresence(text, info, fragmentId, target, context);
}
function reverseTarget(info, blockId){
  if (!info) return null;
  return info.targets.filter(function(target){
    return target.block === blockId;
  })[0] || null;
}
function checkReverseLive(blockId, list, position, context){
  var fragmentId = list[position].fragment;
  var info = NavModel.forwardTargets(DATA, fragmentId);
  var text = live.textContent;
  check(includes(text, DATA.strings.ui.reverseMode), context + ' live mode');
  check(includes(text, DATA.anchors[blockId] || blockId),
        context + ' live target');
  check(includes(text, positionText(position + 1, list.length,
    DATA.unitLabels[fragmentId] || fragmentId)),
    context + ' live position/subject');
  checkPresence(text, info, fragmentId, reverseTarget(info, blockId), context);
}

if (NavModel){
  var last;
  allEntries().forEach(function(entry){
    var info = NavModel.forwardTargets(DATA, entry.id);
    check(info !== null, 'no forward info for ' + entry.id);
    if (!info) return;
    if (info.status === 'mapped')
      check(info.targets.length >= 1, entry.id + ' mapped without target');
    else check(info.targets.length === 0,
               entry.id + ' no-candidate fragment has targets');
    var origin = document.getElementById('btn-' + entry.id);
    check(!!origin, entry.id + ' origin button missing');
    if (!origin) return;
    origin.focus();
    origin.click();
    check(!forwardBar.hidden,
          entry.kind + ' activation did not show forward bar ' + entry.id);
    check(reverseBar.hidden,
          entry.kind + ' activation left reverse bar visible ' + entry.id);
    check(document.activeElement === forwardBar,
          entry.kind + ' activation focus ' + entry.id);
    check(includes(forwardBar.textContent, DATA.strings.ui.forwardMode),
          entry.kind + ' bar mode ' + entry.id);
    check(includes(forwardBar.textContent,
      DATA.unitLabels[entry.id] || entry.id),
      entry.kind + ' bar subject ' + entry.id);
    check(sourceNode(entry.id).classList.contains('hl-frag'),
          entry.kind + ' source highlight ' + entry.id);
    if (info.status === 'mapped'){
      var target = info.targets[0];
      check(document.getElementById(target.block).classList.contains('hl-strong'),
            entry.kind + ' current target highlight ' + entry.id);
      check(includes(forwardBar.textContent, positionText(1,
        info.targets.length, DATA.anchors[target.block] || target.block)),
        entry.kind + ' bar position/target ' + entry.id);
      if (target.note)
        check(includes(forwardBar.textContent, target.note),
              entry.kind + ' bar note ' + entry.id);
      info.targets.slice(0, 5).forEach(function(other, index){
        if (index > 0)
          check(document.getElementById(other.block).classList.contains('hl-soft'),
                entry.kind + ' alternate target highlight ' + entry.id);
      });
    } else check(includes(forwardBar.textContent,
      DATA.strings.ui.noCandidateNotice),
      entry.kind + ' bar no-candidate notice ' + entry.id);
    checkForwardLive(entry.id, info, 0, entry.kind + ' ' + entry.id);
    document.keydown('Escape');
    check(forwardBar.hidden && reverseBar.hidden,
          entry.kind + ' Escape did not clear bars ' + entry.id);
    check(document.activeElement === origin,
          entry.kind + ' Escape did not restore focus ' + entry.id);
    check(live.textContent === DATA.strings.ui.selectionCleared,
          entry.kind + ' Escape announcement ' + entry.id);
    check(!sourceNode(entry.id).classList.contains('hl-frag'),
          entry.kind + ' Escape left source highlight ' + entry.id);
    coverage[entry.kind === 'unit' ? 'units' : 'phrases'] += 1;
  });

  check(NavModel.cycle(0, 4, -1) === 3, 'cycle wrap back');
  check(NavModel.cycle(3, 4, 1) === 0, 'cycle wrap forward');
  Object.keys(DATA.reverse).forEach(function(block){
    last = null;
    NavModel.reverseFragments(DATA, block).forEach(function(entry){
      var match = /^c(\d+)u(\d+)(?:p(\d+))?$/.exec(entry.fragment);
      check(match !== null, 'malformed reverse fragment ' + entry.fragment);
      if (!match) return;
      check((entry.kind === 'unit') === (match[3] === undefined),
            'reverse kind/id mismatch ' + entry.fragment);
      var key = [parseInt(match[1], 10), entry.kind === 'unit' ? 0 : 1,
        parseInt(match[2], 10),
        match[3] === undefined ? -1 : parseInt(match[3], 10)];
      if (last !== null){
        var comparison = 0;
        for (var index = 0; index < key.length && comparison === 0; index++){
          if (key[index] < last[index]) comparison = -1;
          else if (key[index] > last[index]) comparison = 1;
        }
        check(comparison >= 0,
              'reverse not claim/kind/unit/phrase ordered ' + block);
      }
      last = key;
    });
  });
  Object.keys(DATA.claimGates).forEach(function(claimKey){
    check(NavModel.claimGates(DATA, claimKey + 'u0').length ===
      DATA.claimGates[claimKey].length, 'claim gates lookup ' + claimKey);
  });

  var pointerId = Object.keys(DATA.fragments)[0];
  if (pointerId){
    var pointerOrigin = document.getElementById('btn-' + pointerId);
    global.__selectionText = 'selected disclosure text';
    unitPointers[pointerId].click();
    check(forwardBar.hidden, 'text selection did not suppress pointer activation');
    global.__selectionText = '';
    pointerOrigin.focus();
    unitPointers[pointerId].click();
    check(!forwardBar.hidden && document.activeElement === forwardBar,
          'pointer surface did not activate unit');
    document.keydown('Escape');
    check(document.activeElement === pointerOrigin,
          'pointer activation Escape did not restore control focus');
    coverage.pointerActivations += 1;
  }

  var cycleEntry = allEntries().filter(function(entry){
    var info = NavModel.forwardTargets(DATA, entry.id);
    return info.status === 'mapped' && info.targets.length > 1;
  })[0];
  check(!!cycleEntry, 'no multi-candidate selection for cycling test');
  if (cycleEntry){
    var cycleInfo = NavModel.forwardTargets(DATA, cycleEntry.id);
    var cycleOrigin = document.getElementById('btn-' + cycleEntry.id);
    cycleOrigin.click();
    var previous = buttonByLabel(forwardBar, DATA.strings.ui.previous);
    var next = buttonByLabel(forwardBar, DATA.strings.ui.next);
    check(!!previous && !!next, 'forward cycle controls missing');
    if (previous){
      previous.click();
      var lastPosition = cycleInfo.targets.length - 1;
      check(document.getElementById(cycleInfo.targets[lastPosition].block)
        .classList.contains('hl-strong'), 'forward previous did not wrap');
      check(document.getElementById(cycleInfo.targets[0].block)
        .classList.contains('hl-soft'), 'forward wrap lost alternate highlight');
      check(document.activeElement === forwardBar,
            'forward cycle did not restore bar focus');
      checkForwardLive(cycleEntry.id, cycleInfo, lastPosition,
                       'forward previous wrap');
      next = buttonByLabel(forwardBar, DATA.strings.ui.next);
      next.click();
      check(document.getElementById(cycleInfo.targets[0].block)
        .classList.contains('hl-strong'), 'forward next did not wrap');
      checkForwardLive(cycleEntry.id, cycleInfo, 0, 'forward next wrap');
      forwardBar.focus();
      var arrow = document.keydown('ArrowRight');
      check(arrow.defaultPrevented, 'focused forward arrow not captured');
      check(document.getElementById(cycleInfo.targets[1].block)
        .classList.contains('hl-strong'), 'forward arrow did not advance');
      checkForwardLive(cycleEntry.id, cycleInfo, 1, 'forward arrow move');
      cycleOrigin.focus();
      var before = live.textContent;
      arrow = document.keydown('ArrowRight');
      check(!arrow.defaultPrevented, 'unfocused forward arrow captured');
      check(live.textContent === before, 'unfocused forward arrow moved selection');
    }
    document.keydown('Escape');
  }

  var reverseBlock = Object.keys(DATA.reverse).filter(function(block){
    return DATA.reverse[block].length > 1;
  })[0];
  check(!!reverseBlock, 'no multi-fragment reverse selection');
  if (reverseBlock){
    var reverseList = DATA.reverse[reverseBlock];
    var reverseOrigin = document.getElementById('btn-rev-' + reverseBlock);
    reverseOrigin.focus();
    reverseOrigin.click();
    check(!reverseBar.hidden && forwardBar.hidden,
          'reverse activation did not select reverse bar only');
    check(document.activeElement === reverseBar, 'reverse activation focus');
    check(includes(reverseBar.textContent, DATA.strings.ui.reverseMode),
          'reverse bar mode');
    check(includes(reverseBar.textContent,
      DATA.anchors[reverseBlock] || reverseBlock), 'reverse bar target');
    check(includes(reverseBar.textContent, positionText(1, reverseList.length,
      DATA.unitLabels[reverseList[0].fragment] || reverseList[0].fragment)),
      'reverse bar position/subject');
    check(document.getElementById(reverseBlock).classList.contains('hl-frag'),
          'reverse target highlight');
    check(sourceNode(reverseList[0].fragment).classList.contains('hl-strong'),
          'reverse current subject highlight');
    reverseList.slice(1).forEach(function(entry){
      check(sourceNode(entry.fragment).classList.contains('hl-frag-soft'),
            'reverse alternate subject highlight ' + entry.fragment);
    });
    checkReverseLive(reverseBlock, reverseList, 0, 'reverse activation');
    var reversePrevious = buttonByLabel(reverseBar, DATA.strings.ui.previous);
    var reverseNext = buttonByLabel(reverseBar, DATA.strings.ui.next);
    check(!!reversePrevious && !!reverseNext, 'reverse cycle controls missing');
    if (reversePrevious){
      reversePrevious.click();
      var reverseLast = reverseList.length - 1;
      check(sourceNode(reverseList[reverseLast].fragment)
        .classList.contains('hl-strong'), 'reverse previous did not wrap');
      check(sourceNode(reverseList[0].fragment)
        .classList.contains('hl-frag-soft'),
        'reverse wrap lost alternate highlight');
      checkReverseLive(reverseBlock, reverseList, reverseLast,
                       'reverse previous wrap');
      reverseNext = buttonByLabel(reverseBar, DATA.strings.ui.next);
      reverseNext.click();
      check(sourceNode(reverseList[0].fragment).classList.contains('hl-strong'),
            'reverse next did not wrap');
      checkReverseLive(reverseBlock, reverseList, 0, 'reverse next wrap');
      reverseBar.focus();
      var reverseArrow = document.keydown('ArrowRight');
      check(reverseArrow.defaultPrevented, 'focused reverse arrow not captured');
      check(sourceNode(reverseList[1].fragment).classList.contains('hl-strong'),
            'reverse arrow did not advance');
      checkReverseLive(reverseBlock, reverseList, 1, 'reverse arrow move');
      reverseOrigin.focus();
      var reverseBefore = live.textContent;
      reverseArrow = document.keydown('ArrowRight');
      check(!reverseArrow.defaultPrevented, 'unfocused reverse arrow captured');
      check(live.textContent === reverseBefore,
            'unfocused reverse arrow moved selection');
    }
    document.keydown('Escape');
    check(document.activeElement === reverseOrigin,
          'reverse Escape did not restore badge focus');
    coverage.reverseActivations += 1;
  }

  var gateClaim = Object.keys(DATA.claimGates)[0];
  check(!!gateClaim, 'no claim gate for gate interaction');
  if (gateClaim){
    var gate = DATA.claimGates[gateClaim][0];
    var gateOrigin = document.getElementById(
      'btn-gate-' + gateClaim + '-' + gate.gateId);
    gateOrigin.focus();
    gateOrigin.click();
    check(!forwardBar.hidden && reverseBar.hidden, 'claim gate bar selection');
    check(document.activeElement === forwardBar, 'claim gate activation focus');
    check(includes(forwardBar.textContent, DATA.strings.ui.forwardMode),
          'claim gate bar mode');
    check(includes(live.textContent, DATA.strings.ui.forwardMode),
          'claim gate live mode');
    check(includes(live.textContent, DATA.strings.ui.gatePresent),
          'claim gate live presence');
    check(buttonByLabel(forwardBar, DATA.strings.ui.previous) === null &&
      buttonByLabel(forwardBar, DATA.strings.ui.next) === null,
      'claim gate exposed cycling controls');
    var gateBefore = forwardBar.textContent;
    forwardBar.focus();
    var gateArrow = document.keydown('ArrowRight');
    check(!gateArrow.defaultPrevented, 'claim gate captured arrow');
    check(forwardBar.textContent === gateBefore,
          'claim gate changed on arrow navigation');
    var gateChip = forwardBar.querySelector('.claim-gate-chip');
    check(!!gateChip, 'claim gate caution chip missing');
    if (gateChip){
      gateChip.click();
      var gateQuote = gateChip.parentNode.querySelector('.caution-quote');
      check(gateChip.getAttribute('aria-expanded') === 'true',
            'claim gate quote state not expanded');
      check(!!gateQuote && gate.source &&
        gateQuote.textContent === DATA.quotes[gate.source.block],
        'claim gate did not quote pinned source');
      if (gateQuote) coverage.sourceQuotes += 1;
      gateChip.click();
      check(gateChip.getAttribute('aria-expanded') === 'false' &&
        gateChip.parentNode.querySelector('.caution-quote') === null,
        'claim gate quote did not collapse');
    }
    document.keydown('Escape');
    check(document.activeElement === gateOrigin,
          'claim gate Escape did not restore focus');
    coverage.gateActivations += 1;
  }

  var sourceSelection = null;
  allEntries().some(function(entry){
    var info = NavModel.forwardTargets(DATA, entry.id);
    if (info.caution && info.caution.type === 'source-gate'){
      sourceSelection = {entry:entry, info:info, position:0,
        caution:info.caution};
      return true;
    }
    for (var index = 0; index < info.targets.length; index++){
      if (info.targets[index].caution &&
          info.targets[index].caution.type === 'source-gate'){
        sourceSelection = {entry:entry, info:info, position:index,
          caution:info.targets[index].caution};
        return true;
      }
    }
    return false;
  });
  check(!!sourceSelection, 'no fragment/target source caution to expand');
  if (sourceSelection){
    var sourceOrigin = document.getElementById(
      'btn-' + sourceSelection.entry.id);
    sourceOrigin.click();
    for (var step = 0; step < sourceSelection.position; step++){
      var sourceNext = buttonByLabel(forwardBar, DATA.strings.ui.next);
      if (sourceNext) sourceNext.click();
    }
    check(includes(live.textContent, DATA.strings.ui.cautionPresent),
          'source caution live presence');
    var expectedQuote = DATA.quotes[sourceSelection.caution.source.block];
    var quoteFound = false;
    forwardBar.querySelectorAll('.caution-chip').forEach(function(chip){
      if (chip.classList.contains('claim-gate-chip')) return;
      chip.click();
      var quote = chip.parentNode.querySelector('.caution-quote');
      if (quote && quote.textContent === expectedQuote) quoteFound = true;
      chip.click();
    });
    check(quoteFound, 'fragment/target caution did not quote pinned source');
    if (quoteFound) coverage.sourceQuotes += 1;
    document.keydown('Escape');
  }
}

process.stdout.write(JSON.stringify({
  fails:fails, coverage:coverage, runtimeError:runtimeError
}));
"""
    script = (script.replace("@@RUNTIME@@", json.dumps(runtime_source))
              .replace("@@NAVDATA@@", json.dumps(nav_match.group(1)))
              .replace("@@PROBES@@", json.dumps(probe_match.group(1))))
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
        fh.write(script)
        path = fh.name
    try:
        completed = subprocess.run(
            ["node", path], capture_output=True, text=True, timeout=60)
        if completed.returncode != 0:
            raise AssertionError(completed.stderr)
        return json.loads(completed.stdout)
    finally:
        os.unlink(path)


class Acceptance(unittest.TestCase):
    maxDiff = None

    def _assert_active_technical_preview(self, release_policy):
        profile_id, contract = acceptance.release_profile_contract(
            release_policy, acceptance.load_registry(ROOT))
        self.assertEqual(profile_id, "technical-preview")
        self.assertEqual(contract, TECHNICAL_PREVIEW_PROFILE)
        self.assertEqual(
            contract["deferredControls"],
            ["AC-11.observed", "AC-12.observed", "AC-13.observed",
             "AC-15.observed"])
        self.assertEqual(contract["requiredQaRecordFields"], [])
        self.assertEqual(
            contract["compatibilityAuthorization"], "not-authorized")
        return contract

    def _assert_preview_artifact_label(self, html, contract,
                                       require_print_footer=False,
                                       require_profile_metadata=True):
        label = render.esc(contract["artifactLabel"])
        self.assertIn(label, html)
        if require_profile_metadata:
            nav_match = re.search(
                r'<script type="application/json" id="nav-data">'
                r'(.*?)</script>', html, re.S)
            self.assertIsNotNone(nav_match)
            edition = canon.parse_json(nav_match.group(1))["edition"]
            self.assertEqual(edition["releaseProfile"], contract["id"])
            self.assertEqual(
                edition["compatibilityAuthorization"],
                contract["compatibilityAuthorization"])
            self.assertEqual(
                edition["deferredControls"],
                contract["deferredControls"])
        if require_print_footer:
            footer = re.search(r"<footer>.*?</footer>", html, re.S)
            self.assertIsNotNone(footer)
            self.assertIn(label, footer.group(0))

    def _assert_authorized_record(self, record, label):
        self.assertIsInstance(record, dict, label)
        self.assertTrue(
            authority.is_authoritative_operator(
                record.get("operatorKind"), record.get("operator")),
            "%s lacks an identified authorized human/model operator: %r" %
            (label, record))

    def _disposition_release_model(self, base, disposition_fixture, case):
        """Install one fixture case in a complete, release-validated model.

        The checked-in fixture truthfully remains tool-authored. This synthetic
        model explicitly supplies a model authorization only for exercising the
        release predicate; it does not turn fixture provenance into evidence.
        """
        synthetic = copy.copy(base)
        synthetic.relation = copy.deepcopy(base.relation)
        synthetic.binding = synthetic.relation["binding"]
        synthetic.gates = copy.deepcopy(base.gates)

        fixture_gates = {
            gate["gateId"]: gate
            for gate in disposition_fixture["gates"]["gates"]
        }
        selected = copy.deepcopy(case["disposition"])
        fixture_gate = copy.deepcopy(fixture_gates[selected["gateId"]])
        synthetic.gates["gates"].append(fixture_gate)
        synthetic.gates_by_id = {
            gate["gateId"]: gate for gate in synthetic.gates["gates"]
        }

        def authorize(fields, projection):
            fields["reviewState"] = "internally-reviewed"
            fields["migrationState"] = "current"
            fields.pop("migrationReason", None)
            fields["review"] = {
                "by": "synthetic-acceptance-model",
                "operatorKind": "model",
                "date": "2026-07-23",
                "contentHash": synthetic.content_hash(projection),
            }

        if fixture_gate["requiredScope"] == "claim":
            claim_key = selected["subject"]["id"]
            assignment = copy.deepcopy(next(
                gate for gate in synthetic.relation["claimGates"][claim_key]
                if gate["code"] == fixture_gate["code"]))
            assignment["gateId"] = fixture_gate["gateId"]
            synthetic.relation["claimGates"][claim_key].append(assignment)
            authorize(
                assignment,
                synthetic.claim_gate_projection(claim_key, assignment))
            additions = [selected]
        else:
            # Carry the synthetic target gate on an otherwise un-gated target,
            # leaving the live mandatory target evidence intact.
            mapped = synthetic.relation["fragments"]["c2u0"]
            mapped["targets"][1]["caution"] = {
                "gateId": fixture_gate["gateId"],
                "type": "source-gate",
                "code": fixture_gate["code"],
                "source": {
                    "corpus": synthetic.edition["claimCorpus"],
                    **fixture_gate["source"],
                },
            }
            authorize(
                mapped, synthetic.unit_projection("c2u0", mapped))

            valid_target_cases = [
                item for item in disposition_fixture["cases"]
                if item["expect"] == "valid" and
                item["disposition"]["gateId"] == fixture_gate["gateId"]
            ]
            mapped_subject = next(
                item["disposition"]["subject"]["id"]
                for item in valid_target_cases
                if item["evidence"] == "mapped")
            no_candidate_subject = next(
                item["disposition"]["subject"]["id"]
                for item in valid_target_cases
                if item["evidence"] == "counsel-review-required")
            carried = copy.deepcopy(next(
                item["disposition"] for item in valid_target_cases
                if item["disposition"]["subject"]["id"] == mapped_subject))
            no_target = copy.deepcopy(next(
                item["disposition"] for item in valid_target_cases
                if item["disposition"]["subject"]["id"] ==
                no_candidate_subject and
                item["disposition"]["disposition"] == "no-target-recorded"))
            additions = ([selected, no_target]
                         if selected["subject"]["id"] == mapped_subject
                         else [selected, carried])

            displaced_gate = None
            if selected["disposition"] == \
                    "carried-at-fragment-fallback":
                # The fixture fallback must occupy the fragment caution slot.
                # Remove this one subject from its live fragment-scope gate,
                # then re-pin and re-authorize every affected live disposition.
                fallback = synthetic.relation["fragments"][
                    no_candidate_subject]
                displaced_gate = fallback.get("caution", {}).get("gateId")
                if displaced_gate is not None:
                    original_gate = synthetic.gates_by_id[displaced_gate]
                    original_gate["appliesTo"]["fragments"] = [
                        item for item in
                        original_gate["appliesTo"]["fragments"]
                        if item["id"] != no_candidate_subject
                    ]
                    synthetic.relation["dispositions"] = [
                        disposition for disposition in
                        synthetic.relation["dispositions"]
                        if not (
                            disposition["gateId"] == displaced_gate and
                            disposition["subject"]["id"] ==
                            no_candidate_subject)
                    ]
                fallback["caution"] = {
                    "gateId": fixture_gate["gateId"],
                    "type": "source-gate",
                    "code": fixture_gate["code"],
                    "source": {
                        "corpus": synthetic.edition["claimCorpus"],
                        **fixture_gate["source"],
                    },
                }
                synthetic.gates_by_id = {
                    gate["gateId"]: gate
                    for gate in synthetic.gates["gates"]
                }
                if displaced_gate is not None:
                    changed_gate_hash = synthetic.gate_entry_hash(
                        displaced_gate)
                    for disposition in synthetic.relation["dispositions"]:
                        if disposition["gateId"] == displaced_gate:
                            disposition["gateEntryHash"] = changed_gate_hash
                authorize(
                    fallback,
                    synthetic.unit_projection(no_candidate_subject, fallback))

        synthetic.relation["dispositions"].extend(additions)
        for disposition in synthetic.relation["dispositions"]:
            changed_live_gate = (
                selected["disposition"] ==
                "carried-at-fragment-fallback" and
                displaced_gate is not None and
                disposition["gateId"] == displaced_gate)
            if disposition["gateId"].startswith("fx-") or changed_live_gate:
                authorize(
                    disposition,
                    synthetic.disposition_projection(disposition))
        return synthetic

    # ------------------------------------------------------------------
    def test_ac01_census_extraction(self):
        for ed in EDITIONS:
            parameters = fixture(
                "edition_parameters_%s.json" % ed)["edition"]
            m = get_model(ed)
            exact = {
                "editionConfig": "navigator/editions/%s.json" % ed,
                "claimCorpus": m.edition["claimCorpus"],
                "claimSetVersion": m.edition["claimSetVersion"],
                "targetCorpus": m.edition["targetCorpus"],
                "authorityCorpus": m.edition["authorityCorpus"],
                "corpusRegistries": m.edition["corpusRegistries"],
                "census": m.edition["census"],
                "independentClaims": m.edition["independentClaims"],
                "groups": m.edition["groups"],
                "strategyPrefix": m.edition["strategyPrefix"],
                "relationSet": m.edition["relationSet"],
                "gateInventory": m.edition["gateInventory"],
                "dependencyMap": m.edition["dependencyMap"],
                "qaSources": m.edition["qaSources"],
                "qaRegistry": m.edition["qaRegistry"],
                "stringsResource": m.edition["stringsResource"],
                "forbiddenTerms": m.edition["forbiddenTerms"],
                "artifactName": m.edition["artifactName"],
            }
            self.assertEqual(exact, parameters,
                             "%s §3 parameter table drift" % ed)
            census = m.edition["census"]
            per = {str(c.number): len(c.units) for c in m.claims}
            self.assertEqual(len(m.claims), census["claims"])
            self.assertEqual(sum(per.values()), census["units"])
            self.assertEqual(per, census["perClaim"])
            self.assertEqual(
                sorted(n for n, p in m.parents.items() if p is None),
                sorted(m.edition["independentClaims"]))
            wholes = [b for b in m.target_blocks if b.kind == "claim-whole"]
            self.assertEqual({b.id for b in wholes},
                             {"PC%d" % i for i in range(1, 19)})
            headings = {b.label for b in m.target_blocks
                        if b.kind == "heading"}
            for ex in ("Example 1", "Example 2", "Example 3", "Example 4",
                       "Example 5"):
                self.assertIn(ex, headings)
            tables = [b for b in m.target_blocks
                      if b.kind == "table" and "Example 2" in b.label]
            self.assertEqual(len(tables), 3)
            for t in tables:
                self.assertEqual(len(t.rows), 5)
            figures = [b for b in m.target_blocks if b.kind == "figure"]
            self.assertEqual(len(figures), 4)
            pins = m.registry.corpora[m.edition["targetCorpus"]]["files"]
            for f in figures:
                pinned = [d for p, d in pins.items()
                          if p.endswith(f.meta["file"].split("/")[-1])]
                self.assertEqual(pinned, [f.meta["fileDigest"]])

    def test_ac02_lifecycle(self):
        for ed in EDITIONS:
            m = get_model(ed)
            bad = [e for e in get_errors(ed)
                   if e[0] in ("pending", "stale", "content-hash",
                               "completeness")]
            self.assertEqual(bad, [])
            for otype, key, fields, projection in m.iter_owners():
                self.assertEqual(fields.get("reviewState"),
                                 "internally-reviewed", "%s %s" % (otype, key))
                self.assertEqual(fields.get("migrationState"), "current")
                review = fields["review"]
                self.assertTrue(
                    authority.is_authoritative_operator(
                        review.get("operatorKind"), review.get("by")),
                    "%s %s lacks an identified authorized reviewer" %
                    (otype, key))
                self.assertEqual(fields["review"]["contentHash"],
                                 m.content_hash(projection))

    def test_ac03_gate_integrity(self):
        for ed in EDITIONS:
            bad = [e for e in get_errors(ed)
                   if e[0] in ("integrity", "inventory", "disposition",
                               "duplicate")]
            self.assertEqual(bad, [])
        # the five disposition fixtures, incl. the honest no-candidate
        # release and the rejected wrong-scope case
        fx = fixture("dispositions_fixture.json")
        self.assertEqual(fx["fixtureVersion"], "1")
        m = get_model(fx["edition"])
        self.assertEqual(fx["binding"], m.binding)
        inv = validate._load_invariants(m.gw)
        gates = {g["gateId"]: g for g in fx["gates"]["gates"]}
        self.assertEqual(len(fx["cases"]), 5)
        disposition_schema = m.schemas["relation"]["properties"][
            "dispositions"]["items"]
        observed_cases = set()
        for case in fx["cases"]:
            d = case["disposition"]
            self.assertEqual(d["review"]["operatorKind"], "tool")
            self.assertFalse(authority.is_authoritative_operator(
                d["review"]["operatorKind"], d["review"]["by"]))
            self.assertEqual(schema_validate.validate(
                d, disposition_schema, root=m.schemas["relation"]), [])
            projection = case["reviewProjection"]
            subject = d["subject"]
            claim = (m.claim_of(subject["id"])
                     if subject["kind"] == "fragment"
                     else int(subject["id"][1:]))
            saved_binding = m.binding
            saved_chain = m.chain_hashes[claim]
            try:
                m.binding = copy.deepcopy(projection["identity"]["binding"])
                m.chain_hashes[claim] = projection["dependencyChainHash"]
                self.assertEqual(m.disposition_projection(d), projection)
            finally:
                m.binding = saved_binding
                m.chain_hashes[claim] = saved_chain
            self.assertEqual(d["review"]["contentHash"],
                             canon.composite_digest(
                                 "aa11393:review:c1",
                                 projection))
            entry = gates[d["gateId"]]
            evidence = case["evidence"]
            canon.parse_digest(d["subjectHash"])
            observed_cases.add((
                entry["requiredScope"], evidence, d["disposition"],
                case["expect"], case["hasTargets"]))
            permitted = inv.permitted_dispositions(
                entry["requiredScope"], evidence)
            if case["expect"] == "valid":
                self.assertIn(d["disposition"], permitted, case["name"])
                if d["disposition"] in ("no-target-recorded",
                                        "carried-at-fragment-fallback"):
                    # honest no-candidate: releasable without any target
                    self.assertEqual(evidence, "counsel-review-required")
                    self.assertFalse(case["hasTargets"])
            else:
                self.assertNotIn(d["disposition"], permitted, case["name"])

            # A matrix lookup is not release proof. Install the fixture case
            # into a complete current edition, explicitly authorize the
            # synthetic owners, and exercise the real release validator.
            release_model = self._disposition_release_model(m, fx, case)
            release_errors = validate.validate_edition(
                release_model, for_release=True)
            if case["expect"] == "valid":
                self.assertEqual(release_errors, [], case["name"])
            else:
                self.assertEqual(
                    release_errors,
                    [("disposition",
                      "disposition fx-gate-target@c2u0: "
                      "'no-target-recorded' not permitted for target-scope "
                      "gate over a mapped subject")],
                    case["name"])
        self.assertEqual(observed_cases, {
            ("claim", "mapped", "carried-at-required-scope", "valid", True),
            ("target", "mapped", "carried-at-required-scope", "valid", True),
            ("target", "counsel-review-required",
             "carried-at-fragment-fallback", "valid", False),
            ("target", "counsel-review-required", "no-target-recorded",
             "valid", False),
            ("target", "mapped", "no-target-recorded", "invalid", True),
        })
        # totality of the matrix over every reachable configuration
        for scope in ("target", "fragment", "claim"):
            for evidence in ("mapped", "counsel-review-required"):
                self.assertTrue(inv.permitted_dispositions(scope, evidence))

        # Optional inventory entries may omit evidence, but an authored
        # affirmative disposition must still be truthful.  Exercise the live
        # validator so a future optional gate cannot claim a carried caution
        # that is absent.
        optional = copy.copy(m)
        optional.relation = copy.deepcopy(m.relation)
        optional.binding = optional.relation["binding"]
        optional.gates = copy.deepcopy(m.gates)
        optional.gates_by_id = {
            gate["gateId"]: gate for gate in optional.gates["gates"]}
        optional_gate = next(
            gate for gate in optional.gates["gates"]
            if gate["requiredScope"] == "fragment")
        optional_gate["requirement"] = "optional"
        affirmative = next(
            item for item in optional.relation["dispositions"]
            if item["gateId"] == optional_gate["gateId"] and
            item["disposition"] == "carried-at-required-scope")
        optional_subject = affirmative["subject"]["id"]
        optional.relation["fragments"][optional_subject].pop("caution")
        optional_errors = validate.validate_edition(optional)
        self.assertTrue(any(
            code == "integrity" and
            optional_gate["gateId"] in message and
            "optional gate has affirmative" in message
            for code, message in optional_errors), optional_errors)

        # inventory-completeness attestation current (double-sided)
        for ed in EDITIONS:
            m = get_model(ed)
            from lib.currentstate import (  # noqa: E402
                _approval_selection_key, attestation_evidence_problems,
                current_side_digests)
            sides_now = current_side_digests(m)
            atts = [a for a in read_records("attestation")
                    if a["record"]["type"] == "inventory-completeness" and
                    a["record"]["edition"] == ed and
                    not attestation_evidence_problems(
                        a, sides_now, ed)]
            self.assertTrue(
                atts, "no current authorized-operator inventory-completeness "
                "attestation for %s" % ed)
            selected = min(atts, key=_approval_selection_key)
            self._assert_authorized_record(
                selected["record"], "%s inventory-completeness" % ed)
            sides = selected["record"]["sides"]
            reg = m.registry.corpora[m.edition["claimCorpus"]]
            self.assertEqual(sides["claimSet"], reg["files"][reg["primary"]])
            self.assertEqual(sides["gateInventory"],
                             m.gw.read_log[m.edition["gateInventory"]])

    def test_ac04_source_drift(self):
        for ed in EDITIONS:
            bad = [e for e in get_errors(ed) if e[0] == "drift"]
            self.assertEqual(bad, [])
            m = get_model(ed)
            for _, _, fields, _ in m.iter_owners():
                for hkey in ("fragmentTextHash", "claimHash",
                             "gateEntryHash", "subjectHash"):
                    if hkey in fields:
                        self.assertTrue(
                            fields[hkey].startswith(canon.DIGEST_PREFIX))
                        canon.parse_digest(fields[hkey])

    def test_ac05_schema_invariants(self):
        for ed in EDITIONS:
            self.assertEqual(get_errors(ed), [])
            m = get_model(ed)
            leaves = schema_validate.check_axes(m.schemas["relation"])
            schema_validate.check_locator_coverage(m.schemas["relation"])
            excs = [p for p, ship, review, exc in leaves if exc]
            self.assertTrue(excs)
            for p, ship, review, exc in leaves:
                if exc:
                    self.assertTrue(p.rsplit(".", 1)[-1].startswith("block"))

    def test_ac05_authorized_operator_matrix(self):
        cases = (
            ("identified human", "human", "reviewer@example.test", True,
             True),
            ("identified model", "model", "model-run-42", True, True),
            ("tool", "tool", "stamp.py", False, False),
            ("unknown", "service", "worker", False, False),
            ("missing kind", None, "reviewer@example.test", False, False),
            ("malformed kind", [], "reviewer@example.test", False, False),
            ("blank human identity", "human", "  ", True, False),
            ("missing model identity", "model", None, True, False),
        )
        for label, kind, identity, kind_authorized, pair_authorized in cases:
            with self.subTest(label=label):
                self.assertEqual(
                    authority.is_authoritative_operator_kind(kind),
                    kind_authorized)
                self.assertEqual(
                    authority.is_authoritative_operator(kind, identity),
                    pair_authorized)

        from build import operator_id  # noqa: E402
        from lib.currentstate import approval_evidence_problems  # noqa: E402

        for kind in ("human", "model"):
            with self.subTest(environment_kind=kind), mock.patch.dict(
                    os.environ, {
                        "NAV_OPERATOR": "identified-" + kind,
                        "NAV_OPERATOR_KIND": kind,
                    }, clear=True):
                self.assertEqual(
                    operator_id(), ("identified-" + kind, kind))
            record = {
                "approvalStatus": "passed",
                "operator": "identified-" + kind,
                "operatorKind": kind,
                "note": "Final approval evidence.",
            }
            self.assertEqual(approval_evidence_problems(record), [])

        for label, environment in (
                ("tool", {"NAV_OPERATOR": "stamp.py",
                          "NAV_OPERATOR_KIND": "tool"}),
                ("unknown", {"NAV_OPERATOR": "worker",
                             "NAV_OPERATOR_KIND": "service"}),
                ("missing kind", {"NAV_OPERATOR": "reviewer"}),
                ("blank identity", {"NAV_OPERATOR": " ",
                                    "NAV_OPERATOR_KIND": "human"})):
            with self.subTest(rejected_environment=label), \
                    mock.patch.dict(os.environ, environment, clear=True):
                with self.assertRaises(SystemExit):
                    operator_id()

        for kind, identity in (("tool", "stamp.py"),
                               ("service", "worker"),
                               ("human", " ")):
            record = {
                "approvalStatus": "passed",
                "operator": identity,
                "operatorKind": kind,
                "note": "Final approval evidence.",
            }
            self.assertTrue(approval_evidence_problems(record), record)

    def test_ac06_fixtures(self):
        disposition_fixture = fixture("dispositions_fixture.json")
        fixture_model = get_model(disposition_fixture["edition"])
        self.assertEqual(disposition_fixture["fixtureVersion"], "1")
        self.assertEqual(disposition_fixture["binding"],
                         fixture_model.binding)
        self.assertEqual(
            disposition_fixture["gates"]["corpusId"],
            fixture_model.edition["claimCorpus"])
        self.assertEqual(
            disposition_fixture["gates"]["profileDigest"],
            fixture_model.claim_profile_digest)
        self.assertEqual(schema_validate.validate(
            disposition_fixture["gates"], fixture_model.schemas["gates"]), [])

        fixture_gates = {
            gate["gateId"]: gate
            for gate in disposition_fixture["gates"]["gates"]
        }
        for gate in fixture_gates.values():
            anchor = fixture_model.quotable_anchor(gate["source"]["block"])
            self.assertIsNotNone(anchor, gate["gateId"])
            self.assertEqual(gate["source"]["textHash"], anchor.digest)
            for subject in gate["appliesTo"].get("fragments", []):
                self.assertEqual(
                    subject["hash"],
                    fixture_model.units[subject["id"]].digest,
                    "%s/%s" % (gate["gateId"], subject["id"]))
            for subject in gate["appliesTo"].get("claims", []):
                self.assertEqual(
                    subject["claimHash"],
                    fixture_model.agg_hashes[subject["claim"]],
                    "%s/c%d" % (gate["gateId"], subject["claim"]))

        disposition_schema = fixture_model.schemas["relation"]["properties"] \
            ["dispositions"]["items"]
        for case in disposition_fixture["cases"]:
            disposition = case["disposition"]
            gate = fixture_gates[disposition["gateId"]]
            self.assertEqual(schema_validate.validate(
                disposition, disposition_schema,
                root=fixture_model.schemas["relation"]), [])
            self.assertEqual(
                disposition["gateEntryHash"],
                canon.composite_digest(
                    "aa11393:inventory:c1",
                    fixture_model.gate_entry_projection(gate)))
            subject = disposition["subject"]
            if subject["kind"] == "fragment":
                expected_subject_hash = fixture_model.units[
                    subject["id"]].digest
                claim = fixture_model.claim_of(subject["id"])
            else:
                claim = int(subject["id"][1:])
                expected_subject_hash = fixture_model.agg_hashes[claim]
            self.assertEqual(
                disposition["subjectHash"], expected_subject_hash)
            self.assertEqual(
                case["reviewProjection"],
                fixture_model.disposition_projection(disposition))
            self.assertEqual(
                case["reviewProjection"]["dependencyChainHash"],
                fixture_model.chain_hashes[claim])

        lifecycle = {
            "reviewState", "migrationState", "migrationReason", "review",
            "previousTargets", "proposedFrom",
        }

        def semantic(value):
            if isinstance(value, dict):
                return {k: semantic(v) for k, v in value.items()
                        if k not in lifecycle}
            if isinstance(value, list):
                return [semantic(v) for v in value]
            return value

        for ed in EDITIONS:
            name = "%s_excerpt.json" % ed
            fx = fixture(name)
            m = get_model(ed)
            errs = schema_validate.validate(fx, m.schemas["relation"])
            self.assertEqual(errs, [], name)
            self.assertEqual(fx["binding"], m.relation["binding"])
            for fid, frag in fx["fragments"].items():
                self.assertEqual(semantic(frag), semantic(
                    m.relation["fragments"][fid]))
                self.assertEqual(frag["fragmentTextHash"],
                                 m.units[fid].digest)
            for ckey, gates in fx["claimGates"].items():
                self.assertEqual(semantic(gates), semantic(
                    m.relation["claimGates"][ckey]))
            live_dispositions = {
                (d["gateId"], d["subject"]["kind"], d["subject"]["id"]): d
                for d in m.relation["dispositions"]}
            for disp in fx["dispositions"]:
                key = (disp["gateId"], disp["subject"]["kind"],
                       disp["subject"]["id"])
                self.assertEqual(semantic(disp),
                                 semantic(live_dispositions[key]))
            # Fixture lifecycle is a valid, current documentation projection
            # under the running schema; it is not release evidence.
            original = m.relation
            try:
                m.relation = fx
                for otype, key, fields, projection in m.iter_owners():
                    self.assertEqual(fields["migrationState"], "current")
                    self.assertEqual(fields["reviewState"],
                                     "internally-reviewed")
                    self.assertEqual(
                        fields["review"]["contentHash"],
                        m.content_hash(projection), "%s %s" % (otype, key))
            finally:
                m.relation = original
        # this document's examples match the fixture projections
        tdd = file_text(TDD)
        blocks = re.findall(r"```json\n(.*?)```", tdd, re.S)
        self.assertGreaterEqual(len(blocks), 2)
        documented = {
            "na": canon.parse_json(blocks[0]),
            "af": canon.parse_json(blocks[1]),
        }

        def matches(doc, real, path="$"):
            if isinstance(doc, str) and doc.endswith("…"):
                self.assertTrue(
                    isinstance(real, str) and real.startswith(doc[:-1]),
                    "%s: %r !~ %r" % (path, doc, real))
            elif isinstance(doc, dict):
                self.assertIsInstance(real, dict, path)
                for k, v in doc.items():
                    self.assertIn(k, real, "%s.%s" % (path, k))
                    matches(v, real[k], "%s.%s" % (path, k))
            elif isinstance(doc, list):
                self.assertIsInstance(real, list, path)
                self.assertLessEqual(len(doc), len(real), path)
                for i, v in enumerate(doc):
                    matches(v, real[i], "%s[%d]" % (path, i))
            else:
                self.assertEqual(doc, real, path)

        for ed in EDITIONS:
            matches(documented[ed], fixture("%s_excerpt.json" % ed), ed)

    def test_ac07_meta_tests(self):
        # single-digest-path + registry-access AST discipline
        scope = [
            os.path.join(NAV, "__main__.py"),
            os.path.join(NAV, "build.py"),
            os.path.join(NAV, "schema", "invariants.py"),
        ]
        for name in sorted(os.listdir(os.path.join(NAV, "lib"))):
            if name.endswith(".py"):
                scope.append(os.path.join(NAV, "lib", name))
        for path in scope:
            src = file_text(path)
            base = os.path.basename(path)
            if base != "canon.py":
                self.assertNotIn("hashlib", src,
                                 "%s computes digests outside canon" % base)
            # Gateway owns declared pipeline I/O; snapshot owns the separate
            # whole-repository immutability boundary used by verify-current.
            if base not in ("gateway.py", "snapshot.py"):
                self.assertNotRegex(
                    src, r"(?<![\w.])open\(",
                    "%s opens files outside the gateways" % base)

        # Every production JSON input crosses canon.parse_json's closed value
        # domain.  Direct stdlib json.load/json.loads calls are permitted only
        # inside canon.py itself.  Tool sources are runner support inputs, so
        # this registered assertion is byte-bound rather than reading
        # undeclared code.
        json_scope = list(scope)
        tools_root = os.path.join(NAV, "tools")
        json_scope.extend(
            os.path.join(tools_root, name)
            for name in sorted(os.listdir(tools_root))
            if name.endswith(".py"))
        forbidden_json_reads = []
        canon_json_reads = []
        for path in json_scope:
            tree = ast.parse(file_text(path), filename=path)
            module_aliases = set()
            function_aliases = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for imported in node.names:
                        if imported.name == "json":
                            module_aliases.add(imported.asname or "json")
                elif isinstance(node, ast.ImportFrom) and \
                        node.module == "json":
                    for imported in node.names:
                        if imported.name in ("load", "loads"):
                            function_aliases.add(
                                imported.asname or imported.name)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                direct = isinstance(node.func, ast.Name) and \
                    node.func.id in function_aliases
                qualified = isinstance(node.func, ast.Attribute) and \
                    node.func.attr in ("load", "loads") and \
                    isinstance(node.func.value, ast.Name) and \
                    node.func.value.id in module_aliases
                if not (direct or qualified):
                    continue
                finding = "%s:%d" % (
                    os.path.relpath(path, ROOT), node.lineno)
                if os.path.basename(path) == "canon.py":
                    canon_json_reads.append(finding)
                else:
                    forbidden_json_reads.append(finding)
        self.assertTrue(canon_json_reads,
                        "canonical JSON parser boundary was not exercised")
        self.assertEqual(
            forbidden_json_reads, [],
            "production JSON reads bypass canon.parse_json")
        # import direction: a render source never imports a control source,
        # and no production source imports a test module.  Imported names
        # resolve against the two closed inventories ("navigator/" stripped,
        # lib/x.py -> lib.x, build.py -> build, tests/*.py -> tests helpers);
        # from-imports resolve against the importer's package at any level.
        def direction_module_name(relpath):
            parts = relpath.split("/")
            if parts[0] == "navigator":
                parts = parts[1:]
            if parts[-1] == "__init__.py":
                parts = parts[:-1]
            elif parts[-1].endswith(".py"):
                parts[-1] = parts[-1][:-3]
            return ".".join(parts)

        render_modules = {
            direction_module_name(path)
            for path in render_inventory.RENDER_SOURCE_PATHS}
        control_modules = {
            direction_module_name(path)
            for path in control_inventory.CONTROL_SOURCE_PATHS}
        test_modules = {"tests"}
        for name in os.listdir(os.path.join(NAV, "tests")):
            if name.endswith(".py"):
                test_modules.add(name[:-3])
                test_modules.add("tests." + name[:-3])
        direction_problems = []
        for path in scope:
            relpath = os.path.relpath(path, ROOT).replace(os.sep, "/")
            importer = direction_module_name(relpath)
            tree = ast.parse(file_text(path), filename=path)
            for node in ast.walk(tree):
                imported = []
                if isinstance(node, ast.Import):
                    imported = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    package = importer.split(".")[:-1]
                    if node.level:
                        package = package[:len(package) - node.level + 1]
                    base = ".".join(
                        package + ([node.module] if node.module else []))
                    imported = [base] if base else []
                    imported.extend(
                        "%s.%s" % (base, alias.name) if base else alias.name
                        for alias in node.names)
                for name in imported:
                    normalized = name
                    if normalized.startswith("navigator."):
                        normalized = normalized[len("navigator."):]
                    if normalized in test_modules:
                        direction_problems.append(
                            "%s:%d imports test module %s"
                            % (relpath, node.lineno, name))
                    elif importer in render_modules and \
                            normalized in control_modules:
                        direction_problems.append(
                            "%s:%d render source imports control source %s"
                            % (relpath, node.lineno, name))
        self.assertEqual(direction_problems, [],
                         "import direction violations")
        # edition-blindness: shared modules contain no edition tokens
        for path in scope:
            base = os.path.basename(path)
            src = file_text(path)
            for token in ("na-claims", "af-claims", "na-v2", "af-v2",
                          "normal-allowance", "allowance-first",
                          "NA edition", "AF edition", "na_", "af_"):
                self.assertNotIn(token, src,
                                 "%s contains edition token %r" % (base, token))
        # Every production module has exactly one trust boundary. Renderer
        # sources bind artifacts; control sources bind acceptance receipts.
        production_paths = {
            os.path.relpath(path, ROOT).replace(os.sep, "/") for path in scope
        }
        self.assertEqual(
            set(render_inventory.RENDER_SOURCE_PATHS) |
            set(control_inventory.CONTROL_SOURCE_PATHS), production_paths)
        self.assertFalse(
            set(render_inventory.RENDER_SOURCE_PATHS) &
            set(control_inventory.CONTROL_SOURCE_PATHS))
        for ed in EDITIONS:
            declared_inputs = get_model(ed).edition[
                "declaredTransitiveInputs"]
            declared_python = {
                path for path in declared_inputs if path.endswith(".py")}
            self.assertEqual(
                declared_python, set(render_inventory.RENDER_SOURCE_PATHS),
                "%s render source inventory is not exact" % ed)
            self.assertEqual(
                projections.render_source_paths(declared_inputs),
                render_inventory.RENDER_SOURCE_PATHS)
        # writer-set: a full derivation writes nothing to the content plane
        m = get_model(EDITIONS[0])
        inputs = m.edition["declaredTransitiveInputs"]
        before = {p: canon.bytes_digest(file_bytes(os.path.join(ROOT, p)))
                  for p in inputs}
        render.render(m, mode="candidate")
        after = {p: canon.bytes_digest(file_bytes(os.path.join(ROOT, p)))
                 for p in inputs}
        self.assertEqual(before, after)
        # diff-classifier: migrate on a re-anchored corpus touches locator
        # fields only (class b) — simulated by digest-preserving anchor swap
        from lib import migrate as migrate_mod
        boot = gateway.ContentGateway(ROOT)
        epath = "navigator/editions/%s.json" % EDITIONS[0]
        allow = canon.parse_json(boot.read_text(epath))[
            "declaredTransitiveInputs"]
        m2 = model.EditionModel(
            gateway.ContentGateway(ROOT, allowlist=allow), epath)
        for _, _, fields, projection in m2.iter_owners():
            fields["review"]["contentHash"] = m2.content_hash(projection)
        rel_before = copy.deepcopy(m2.relation)
        log = []
        migrate_mod.migrate_inventory(m2, log)
        migrate_mod.migrate_relation(m2, log)
        self.assertEqual(log, [])  # pinned corpora: nothing to do
        self.assertEqual(rel_before, m2.relation)
        # procedure-vs-matrix: §10 privilege table + §13 procedure prose
        # against planes.json — prose is checked, not trusted
        planes = m.planes
        tdd = file_text(TDD)
        matrix = tdd[tdd.index("| Command | Reads (kinds) | Writes (kinds) |"):]
        matrix = matrix.split("\n\n")[0] + "\n"
        rows = re.findall(r"\| `([a-z-]+)`( \(deferred\))? \| (.*?) \| (.*?) \|\n",
                          matrix)
        self.assertEqual(len(rows), 13)
        for cmd, deferred, reads, writes in rows:
            self.assertIn(cmd, planes["commands"], cmd)
            command = planes["commands"][cmd]
            prose_reads = set(re.findall(r"`([a-z][a-z:-]+)`", reads))
            prose_writes = set(re.findall(r"`([a-z][a-z:-]+)`", writes))
            self.assertEqual(prose_reads, set(command["reads"]),
                             "%s read-kind set drift" % cmd)
            self.assertEqual(prose_writes, set(command["writes"]),
                             "%s write-kind set drift" % cmd)
            self.assertEqual(bool(deferred), bool(command.get("deferred")),
                             "%s deferred marker drift" % cmd)
            if "contentScope" in command:
                scope = command["contentScope"].replace("-", " ")
                self.assertIn(scope, reads.replace("-", " "),
                              "%s content scope drift" % cmd)
        proc = tdd[tdd.index("Normative update procedure"):]
        proc = proc[:proc.index("## 14.")]
        for cmd in ("candidate", "migrate", "record-qa", "release",
                    "bundle-plan", "bundle", "verify-current"):
            self.assertIn(cmd, proc)
        self.assertIn("release-record",
                      planes["commands"]["release"]["writes"])
        self.assertIn("bundle-record", planes["commands"]["bundle"]["writes"])
        for kind, plane in planes["kinds"].items():
            self.assertIn(plane, ("artifact", "verification"))
        artifact_kinds = {
            kind for kind, plane in planes["kinds"].items()
            if plane == "artifact"
        }
        self.assertEqual(
            artifact_kinds, set(gateway.ARTIFACT_PATH_POLICIES),
            "every artifact kind needs one central path policy")
        representative_paths = {
            "preview": "preview_release.html",
            "candidate": "candidate_release.html",
            "sealed": "release.html",
            "artifact-checksum": "release.html.sha256",
            "bundle": "delivery.zip",
            "bundle-checksum": "delivery.zip.sha256",
            "bundle-manifest": "MANIFEST.txt",
        }
        for kind, path in representative_paths.items():
            self.assertEqual(gateway.validate_artifact_path(kind, path), path)
            for other_kind in artifact_kinds - {kind}:
                with self.assertRaises(
                        gateway.GatewayError,
                        msg="%s path was accepted as %s" % (kind, other_kind)):
                    gateway.validate_artifact_path(other_kind, path)
        for alias in ("navigator/schema/../relations/example.json",
                      "./navigator/relations/example.json",
                      "navigator\\relations\\example.json"):
            with self.assertRaises(gateway.GatewayError):
                gateway.ContentGateway(ROOT, allowlist=[alias])
        for duplicates in (("navigator/build.py", "navigator/build.py"),
                           ("Navigator/build.py", "navigator/build.py")):
            with self.assertRaises(gateway.GatewayError):
                gateway.ContentGateway(ROOT, allowlist=duplicates)

    # -- AC-07: migration case-table scenarios (mutated corpus copies) ----

    def _migration_snapshot(self):
        return fixture("migration_na_snapshot.json")

    def _migration_tree(self, tmp):
        """Materialize the locked synthetic NA snapshot in a temp tree."""
        import shutil
        snapshot = self._migration_snapshot()
        for d in ("navigator/schema", "navigator/lib"):
            shutil.copytree(os.path.join(ROOT, d), os.path.join(tmp, d),
                            ignore=shutil.ignore_patterns("__pycache__"))
        build_path = os.path.join(tmp, "navigator", "build.py")
        os.makedirs(os.path.dirname(build_path), exist_ok=True)
        shutil.copy(os.path.join(NAV, "build.py"), build_path)
        for rel, encoded in snapshot["files"].items():
            dst = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "wb") as fh:
                fh.write(base64.b64decode(encoded, validate=True))
        # Migration behavior is tested from a synthetic, current baseline.
        # The checked-in relation may legitimately be stale while a reviewed
        # projection change is in flight, so do not inherit its lifecycle
        # flags into this isolated baseline.  This reset/restamp is test
        # setup, not evidence, and never touches the repository's records.
        relation_path = os.path.join(tmp, snapshot["relationPath"])
        with open(relation_path, encoding="utf-8") as fh:
            relation = json.load(fh)

        def reset_lifecycle(owner):
            owner["migrationState"] = "current"
            owner.pop("migrationReason", None)
            owner.pop("previousTargets", None)

        for fragment in relation["fragments"].values():
            reset_lifecycle(fragment)
            for phrase in fragment.get("phrases", []):
                reset_lifecycle(phrase)
        for gate_list in relation["claimGates"].values():
            for gate in gate_list:
                reset_lifecycle(gate)
        for disposition in relation["dispositions"]:
            reset_lifecycle(disposition)
        with open(relation_path, "w", encoding="utf-8") as fh:
            json.dump(relation, fh, indent=1, ensure_ascii=False)
            fh.write("\n")

        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "baseline_stamp_tool", os.path.join(NAV, "tools", "stamp.py"))
        stamp_tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stamp_tool)
        cwd = os.getcwd()
        try:
            stamp_tool.stamp(
                tmp, snapshot["editionPath"], stamp_inventory=True)
            stamp_tool.stamp(
                tmp, snapshot["editionPath"], mark_reviewed=True,
                all_owners=True, reviewer="synthetic-test-reviewer",
                review_date="2026-07-22", operator_kind="human")
        finally:
            os.chdir(cwd)
        return tmp

    def _mutate(self, tmp, rel, edits):
        path = os.path.join(tmp, rel)
        with open(path, encoding="utf-8") as fh:
            s = fh.read()
        for old, new in edits:
            self.assertIn(old, s, "mutation target not found: %r" % old[:60])
            s = s.replace(old, new, 1)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(s)

    def _repin(self, tmp, *rels):
        with open(os.path.join(
                tmp, self._migration_snapshot()["editionPath"]),
                  encoding="utf-8") as fh:
            config = json.load(fh)
        registries = []
        for relative in config["corpusRegistries"]:
            cpath = os.path.join(tmp, relative)
            with open(cpath, encoding="utf-8") as fh:
                registries.append((cpath, json.load(fh)))
        for rel in rels:
            with open(os.path.join(tmp, rel), "rb") as fh:
                digest = canon.bytes_digest(fh.read())
            for unused_path, reg in registries:
                for entry in reg["corpora"].values():
                    if rel in entry["files"]:
                        entry["files"][rel] = digest
        for cpath, reg in registries:
            with open(cpath, "w", encoding="utf-8") as fh:
                json.dump(reg, fh, indent=1, ensure_ascii=False)

    def _migrated(self, tmp):
        from lib import migrate as migrate_mod
        gw = gateway.ContentGateway(tmp)
        m = model.EditionModel(
            gw, self._migration_snapshot()["editionPath"])
        before_relation = copy.deepcopy(m.relation)
        before_inventory = copy.deepcopy(m.gates)
        log = []
        migrate_mod.migrate_inventory(m, log)
        migrate_mod.migrate_relation(m, log)
        return m, log, before_relation, before_inventory

    def test_ac07_migration_scenarios(self):
        import tempfile
        snapshot = self._migration_snapshot()
        claim_path = snapshot["claimPath"]
        target_path = snapshot["targetPath"]
        relation_path = snapshot["relationPath"]
        gate_path = snapshot["gateInventoryPath"]
        edition_path = snapshot["editionPath"]
        # ---- scenario 1: every mechanically reachable case-table row ----
        with tempfile.TemporaryDirectory() as tmp:
            self._migration_tree(tmp)
            self._mutate(tmp, target_path, [
                # shift all later disclosure anchors (re-anchoring, class b)
                ("### Field of the invention\n\n",
                 "### Field of the invention\n\nA synthetic migration-test "
                 "paragraph inserted to shift subsequent anchors.\n\n"),
                # target block text changed
                ("the streamed content in the form of said chunks 113 is "
                 "distributed using unicasting.",
                 "the streamed content in the form of said chunks 113 is "
                 "distributed using unicasting (edited for the migration "
                 "scenario)."),
                # mid-document deletion: digest vanishes, locator re-filled
                ("In a preferred embodiment of the present invention, a "
                 "single time code variation is applied at each "
                 "director-commanded camera cut to ensure each content mate "
                 "remains unique and traceable.\n\n", ""),
                # repeated text: duplicate a targeted block
                ("In some embodiments of the present invention, said record "
                 "is a ledger 122.\n",
                 "In some embodiments of the present invention, said record "
                 "is a ledger 122.\n\nIn some embodiments of the present "
                 "invention, said record is a ledger 122.\n"),
            ])
            self._mutate(tmp, claim_path, [
                # fragment text changed (claim 1 -> dependents cascade)
                ("receive video captured from a plurality of cameras and a "
                 "structured list of instructions describing edits",
                 "receive video captured from a plurality of cameras "
                 "together with a structured list of instructions "
                 "describing edits"),
                # fragment removed (claim 9 loses a delivery unit)
                ("cause delivery, to respective recipients, of audio-video "
                 "streams assembled according to respective manifest files; "
                 "and\n\n", ""),
                # new fragment appears (claim 30 gains a unit); anchor on the
                # full claim-30 text — claim 8 shares the trailing words
                ("**30.** The method of claim 22, further comprising "
                 "overlaying one or more additional audio or video elements "
                 "not present in the video received from the plurality of "
                 "cameras onto at least one of the reference audio-video "
                 "content or the mate before segmenting the ensemble.\n",
                 "**30.** The method of claim 22, further comprising "
                 "overlaying one or more additional audio or video elements "
                 "not present in the video received from the plurality of "
                 "cameras onto at least one of the reference audio-video "
                 "content or the mate before segmenting the ensemble.\n\n"
                 "wherein the overlaying is "
                 "performed before delivery of the respective versions.\n"),
                # shift guidance anchors (inventory source re-anchoring)
                ("## 2. Drafting principles\n\n",
                 "## 2. Drafting principles\n\nA synthetic migration-test "
                 "note inserted to shift guidance anchors.\n\n"),
                # caution-source block text changed
                ("Example 2 directly shows Camera 2 followed by Camera 3, "
                 "extension of Camera 2, delayed commencement of Camera 3, "
                 "and noncoincident transition timings.",
                 "Example 2 directly shows Camera 2 followed by Camera 3, "
                 "extension of Camera 2, delayed commencement of Camera 3, "
                 "and noncoincident transition timings (edited for the "
                 "migration scenario)."),
            ])
            self._repin(tmp, target_path, claim_path)
            m, log, before_relation, before_inventory = \
                self._migrated(tmp)
            rel = m.relation
            from lib import migrate as migrate_mod
            self.assertEqual(migrate_mod.migration_diff_problems(
                before_relation, rel, before_inventory, m.gates), [])

            illegal_semantic = copy.deepcopy(rel)
            illegal_semantic["fragments"]["c17u0"]["status"] = \
                "counsel-review-required"
            semantic_problems = migrate_mod.migration_diff_problems(
                before_relation, illegal_semantic,
                before_inventory, m.gates)
            self.assertTrue(any(
                "status" in problem and "outside action classes" in problem
                for problem in semantic_problems), semantic_problems)

            illegal_review = copy.deepcopy(rel)
            illegal_review["fragments"]["c17u0"]["review"]["by"] = \
                "unauthorized-migration"
            review_problems = migrate_mod.migration_diff_problems(
                before_relation, illegal_review,
                before_inventory, m.gates)
            self.assertTrue(any(
                "review" in problem and "outside action classes" in problem
                for problem in review_problems), review_problems)
            reasons = {fid: (rel["fragments"][fid].get("migrationState"),
                             rel["fragments"][fid].get("migrationReason"))
                       for fid in rel["fragments"]}
            # mechanical re-anchoring: locators updated, review untouched
            self.assertTrue(any(a == "re-anchor" for a, _, _ in log))
            c17 = rel["fragments"]["c17u0"]
            self.assertEqual(c17["migrationState"], "current")
            self.assertEqual(c17["reviewState"], "internally-reviewed")
            for t in c17["targets"]:
                anchor = m.target_anchor(t["block"])
                self.assertEqual(anchor.digest, t["textHash"])
            # inventory: unique-match re-anchor vs unresolved manual
            self.assertTrue(any(
                action == "re-anchor" and key.startswith("inventory:")
                for action, key, unused_detail in log))
            self.assertIn(("manual", "inventory:na-gate-production-relationship"),
                          [(a, k) for a, k, _ in log])
            # case rows
            self.assertEqual(reasons["c1u1"], ("stale", "changed"))
            self.assertTrue(rel["fragments"]["c1u1"].get("previousTargets"))
            self.assertEqual(reasons["c14u0"], ("stale", "target-changed"))
            self.assertTrue(rel["fragments"]["c14u0"].get("previousTargets"))
            # mid-document deletion mechanically classifies as target-changed
            # (removal is observable only at a container tail — TDD §10.6)
            self.assertEqual(reasons["c6u0"], ("stale", "target-changed"))
            self.assertEqual(reasons["c12u0"], ("stale", "ambiguous"))
            self.assertEqual(reasons["c9u7"], ("stale", "changed"))
            self.assertEqual(reasons["c9u8"],
                             ("stale", "fragment-removed"))
            # Unaffected fragments remain current despite surrounding shifts.
            self.assertEqual(reasons["c16u5"], ("current", None))
            self.assertEqual(reasons["c22u6"], ("current", None))
            # ancestor-claim change cascades to dependents
            self.assertEqual(reasons["c5u0"], ("stale", "endpoint-changed"))
            gate_c1 = rel["claimGates"]["c1"][0]
            self.assertEqual((gate_c1["migrationState"],
                              gate_c1.get("migrationReason")),
                             ("stale", "source-changed"))
            # new fragment appears as counsel-review-required + pending
            self.assertIn("c30u1", rel["fragments"])
            self.assertEqual(rel["fragments"]["c30u1"]["status"],
                             "counsel-review-required")
            self.assertEqual(rel["fragments"]["c30u1"]["reviewState"],
                             "pending")
            # re-anchored caution sources did NOT invalidate dispositions
            # (gate-entry hash excludes the source locator)
            prio = [d for d in rel["dispositions"]
                    if d["gateId"] == "na-gate-example2-resynchronization" and
                    d["subject"]["id"] == "c23u0"]
            self.assertEqual(prio[0]["migrationState"], "current")
            # but the parent-claim amendment cascades to c2's disposition
            prio2 = [d for d in rel["dispositions"]
                     if d["gateId"] ==
                     "na-gate-example2-resynchronization" and
                     d["subject"]["id"] == "c2u0"]
            self.assertEqual((prio2[0]["migrationState"],
                              prio2[0].get("migrationReason")),
                             ("stale", "endpoint-changed"))

            # ---- §13 steps 4-5: resolve every stale/pending, restamp,
            # and reach a green candidate on the mutated tree -------------
            def find_block(snippet, quotable=False):
                order = m.guidance_order if quotable else m.target_order
                cls = "quotable" if quotable else "targetable"
                hits = [a for a in order if a.cls == cls and
                        snippet in (a.block.canonical or "")]
                self.assertEqual(len(hits), 1, snippet)
                return hits[0]

            def dead(x):
                anchor = m.target_anchor(x["block"])
                return anchor is None or anchor.digest != x["textHash"]

            frags = rel["fragments"]
            # target-changed: the human re-targets to the edited block
            t = [x for x in frags["c14u0"]["targets"] if dead(x)][0]
            t["block"] = find_block(
                "unicasting (edited for the migration scenario)").id
            # vanished-digest target: drop the dead candidate, keep survivors
            frags["c6u0"]["targets"] = [
                x for x in frags["c6u0"]["targets"] if not dead(x)]
            self.assertTrue(frags["c6u0"]["targets"])
            # ambiguous: the human picks one occurrence
            for fid in ("c12u0", "c16u5"):
                for x in frags[fid].get("targets", []):
                    if dead(x):
                        positions = m.digest_positions.get(x["textHash"], [])
                        self.assertGreater(len(positions), 1, fid)
                        x["block"] = positions[0]
            # fragment removed: delete the entry in the resolving commit
            del frags["c9u8"]
            # new fragment: author the honest no-candidate entry
            frags["c30u1"]["review"].update(by="scenario-review",
                                            date="2026-07-22")
            # caution source: re-point the inventory at the edited block
            m.gates_by_id[
                "na-gate-production-relationship"]["source"]["block"] = \
                find_block("(edited for the migration scenario)",
                           quotable=True).id
            # resolving review: lifecycle reset (restamp re-reviews below)
            def reset(owner):
                owner["migrationState"] = "current"
                owner.pop("migrationReason", None)
            for frag in frags.values():
                reset(frag)
                for ph in frag.get("phrases", []):
                    reset(ph)
            for gl in rel["claimGates"].values():
                for g in gl:
                    reset(g)
            for d in rel["dispositions"]:
                reset(d)
            # census follows the amended claim set (git-reviewed edit)
            epath = os.path.join(tmp, edition_path)
            with open(epath, encoding="utf-8") as fh:
                ecfg = json.load(fh)
            ecfg["census"]["perClaim"]["9"] = 8
            ecfg["census"]["perClaim"]["30"] = 2
            with open(epath, "w", encoding="utf-8") as fh:
                json.dump(ecfg, fh, indent=1, ensure_ascii=False)
            for relpath, obj in ((relation_path, rel),
                                 (gate_path, m.gates)):
                with open(os.path.join(tmp, relpath), "w",
                          encoding="utf-8") as fh:
                    json.dump(obj, fh, indent=1, ensure_ascii=False)
            # restamp endpoint pins + fresh contentHashes, marked reviewed
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "stamp_tool", os.path.join(NAV, "tools", "stamp.py"))
            stamp_tool = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(stamp_tool)
            cwd = os.getcwd()
            try:
                stamp_tool.stamp(
                    tmp, edition_path, stamp_inventory=True)
                stamp_tool.stamp(tmp, edition_path,
                                 mark_reviewed=True, all_owners=True,
                                 reviewer="synthetic-test-reviewer",
                                 review_date="2026-07-22",
                                 operator_kind="human")
            finally:
                os.chdir(cwd)
            # the resolved edition validates clean and yields a candidate
            gw2 = gateway.ContentGateway(tmp)
            m2 = model.EditionModel(gw2, edition_path)
            self.assertTrue(m2.relation["fragments"]["c14u0"]
                            .get("previousTargets"))
            self.assertEqual(validate.validate_edition(m2), [])
            self.assertEqual(validate.validate_edition(m2, for_release=True),
                             [])
            resolved = render.render(m2, mode="candidate")
            self.assertTrue(resolved.startswith(b"<!DOCTYPE html>"))
            self.assertGreater(len(resolved), 100_000)
        # ---- scenario 2: target removed (container-tail deletion) -------
        with tempfile.TemporaryDirectory() as tmp:
            self._migration_tree(tmp)
            path = os.path.join(tmp, target_path)
            with open(path, encoding="utf-8") as fh:
                s = fh.read()
            cut = s.index("**16.** Method (200)")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(s[:cut])
            self._repin(tmp, target_path)
            m, log, before_relation, before_inventory = \
                self._migrated(tmp)
            from lib import migrate as migrate_mod
            self.assertEqual(migrate_mod.migration_diff_problems(
                before_relation, m.relation,
                before_inventory, m.gates), [])
            c22u0 = m.relation["fragments"]["c22u0"]
            self.assertEqual((c22u0["migrationState"],
                              c22u0.get("migrationReason")),
                             ("stale", "target-removed"))
        # ---- scenario 3: canonVersion mismatch fails before any write ----
        with tempfile.TemporaryDirectory() as tmp:
            self._migration_tree(tmp)
            from lib import migrate as migrate_mod
            rpath = os.path.join(tmp, relation_path)
            with open(rpath, encoding="utf-8") as fh:
                relx = json.load(fh)
            relx["binding"]["canonVersion"] = "c0"
            with open(rpath, "w", encoding="utf-8") as fh:
                json.dump(relx, fh, indent=1, ensure_ascii=False)
            with self.assertRaises(model.ModelError):
                model.EditionModel(
                    gateway.ContentGateway(tmp), edition_path)
            with open(rpath, "rb") as fh:
                before_relation_bytes = fh.read()
            with open(os.path.join(tmp, gate_path), "rb") as fh:
                before_gate_bytes = fh.read()
            child = subprocess.run(
                [sys.executable, os.path.join(tmp, "navigator", "build.py"),
                 "migrate", "na", "--private-runner"],
                cwd=tmp, capture_output=True, text=True, timeout=300)
            self.assertNotEqual(child.returncode, 0)
            self.assertIn("invalid relation set", child.stderr)
            with open(rpath, "rb") as fh:
                self.assertEqual(fh.read(), before_relation_bytes)
            with open(os.path.join(tmp, gate_path), "rb") as fh:
                self.assertEqual(fh.read(), before_gate_bytes)

    def test_ac07_hard_current_boundary(self):
        from lib import currentstate

        # Obsolete primary-strategy versions fail, while the distinct
        # continuation strategy namespace cannot be mistaken for AF.
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "docs"))
            with open(os.path.join(root, "docs", "versions.md"), "w",
                      encoding="utf-8") as fh:
                fh.write(
                    "NA-2026-07-22-v4 " + "AF-" + "2026-07-21-v5 "
                    "AF-CONT-2026-07-20-v2\n")
            content = gateway.ContentGateway(root)
            with mock.patch.object(currentstate, "ROOT", root):
                version_problems = currentstate._live_version_problems(
                    content, {
                        "NA": "NA-2026-07-22-v4",
                        "AF": "AF-2026-07-22-v6",
                    })
        self.assertTrue(any("obsolete AF version" in problem
                            for problem in version_problems),
                        version_problems)
        self.assertFalse(any("AF-CONT" in problem
                             for problem in version_problems),
                         version_problems)

        inventory_problems = currentstate._exact_inventory_problems(
            {"current", "orphan"}, {"current", "required"}, "dist")
        self.assertTrue(any("orphan" in problem
                            for problem in inventory_problems))
        self.assertTrue(any("required" in problem
                            for problem in inventory_problems))
        self.assertTrue(recordprovenance.current_record_format_problems(
            "release-record", {
                "edition": EDITIONS[0], "sealed": "retired.html"}))

        for edition in EDITIONS:
            with self.subTest(edition=edition):
                self.assertEqual(currentstate._pin_plan_problems(
                    currentstate.current_pin_plan(edition)), [])

        command = get_model(EDITIONS[0]).planes["commands"][
            "verify-current"]
        self.assertEqual(command["writes"], [])
        self.assertEqual(set(command["reads"]), {
            "content", "candidate", "sealed", "artifact-checksum",
            "bundle", "bundle-manifest", "bundle-checksum", "qa-record",
            "attestation", "release-record", "bundle-record",
        })

        # Full-repository and bundle acceptance runs select both editions;
        # standalone releases select one and must not read the inactive side.
        if len(EDITIONS) == currentstate.DELIVERY_EDITION_COUNT:
            content = gateway.ContentGateway(ROOT)
            self.assertEqual(
                currentstate._classified_navigator_source_problems(
                    content, currentstate.delivery_edition_ids()), [])

    def test_ac08_projections(self):
        for ed in EDITIONS:
            m = get_model(ed)
            relation_schema = m.schemas["relation"]
            never_paths = _schema_ship_paths(
                relation_schema, relation_schema, "never")
            self.assertTrue(never_paths)

            # Exercise every currently declared never path, including optional
            # opaque containers, without a hand-maintained field blacklist.
            markers = {}
            never_only = _never_only_instance(
                relation_schema, relation_schema, markers)
            self.assertEqual(set(markers), never_paths)
            for projection_mode in ("artifact", "schedule"):
                projected_synthetic = schema_validate.ship_axis(
                    relation_schema, never_only, projection_mode)
                self.assertEqual(projected_synthetic, {})
                serialized = json.dumps(projected_synthetic)
                for marker in markers.values():
                    self.assertNotIn(marker, serialized)

                projected_live = schema_validate.ship_axis(
                    relation_schema, m.relation, projection_mode)
                self.assertEqual(_ship_axis_leaks(
                    projected_live, relation_schema, relation_schema), [])

            qa_registry = currentstate.edition_qa_registry(m)
            internal_tokens = {"qa-source"}
            for corpus_id, entry in qa_registry.corpora.items():
                internal_tokens.add(corpus_id)
                internal_tokens.add(entry["primary"])
                internal_tokens.update(entry["files"])
                internal_tokens.update(entry["files"].values())

            for mode in ("candidate", "preview"):
                html = get_html(ed, mode).decode("utf-8")
                nav_match = re.search(
                    r'<script type="application/json" id="nav-data">'
                    r'(.*?)</script>', html, re.S)
                self.assertIsNotNone(nav_match)
                nav_data = canon.parse_json(nav_match.group(1))
                shipped = projections.ship_relation(m, "artifact")
                self.assertEqual(nav_data["fragments"], shipped["fragments"])
                self.assertEqual(
                    nav_data["claimGates"], shipped.get("claimGates", {}))
                self.assertEqual(
                    nav_data["claimDispositions"],
                    shipped.get("claimDispositions", {}))
                lowered = html.lower()
                for token in internal_tokens:
                    self.assertNotIn(
                        token.lower(), lowered,
                        "%s %s leaks internal QA identifier %r" %
                        (ed, mode, token))
            # schedule projection = artifact + rationale only
            ship = projections.ship_relation(m, "artifact")
            self.assertNotIn("rationale", json.dumps(ship))

    def test_ac09_escaping(self):
        payloads = fixture("escaping_fixture.json")["payloads"]
        # Context primitives remain defense-in-depth checks.
        for payload in payloads:
            self.assertNotIn(payload, render.esc(payload))
            out = render.esc(payload)
            self.assertNotIn("<script", out.lower())
            self.assertNotIn("<img", out.lower())
            self.assertNotIn('"', out.replace("&quot;", ""))
        # embedded JSON channel: </script never appears unescaped
        blob = render.script_json({"x": payloads})
        self.assertNotIn("</script", blob)
        self.assertNotIn("<", blob.split('"x"', 1)[1].split("]", 1)[0]
                         .replace("\\u003c", ""))
        # md_inline never introduces tags beyond strong/code
        for payload in payloads:
            out = render.md_inline(payload)
            for tag in re.findall(r"<(/?[a-zA-Z]+)", out):
                self.assertIn(tag.lstrip("/"), ("strong", "code"))

        # Put the complete adversarial corpus through the real renderer's four
        # source-controlled channels: note, rationale, phrase text, and quoted
        # source text. The cloned model is deliberately not release evidence.
        adversarial = "\n".join(
            "AC09[%d] %s" % (index, payload)
            for index, payload in enumerate(payloads))
        for ed in EDITIONS:
            base = get_model(ed)
            synthetic = copy.copy(base)
            synthetic.relation = copy.deepcopy(base.relation)
            synthetic.binding = synthetic.relation["binding"]
            synthetic.claims = copy.deepcopy(base.claims)
            synthetic.claims_by_number = {
                claim.number: claim for claim in synthetic.claims
            }
            synthetic.units = {
                unit.id: unit for claim in synthetic.claims
                for unit in claim.units
            }

            target_fid, target = next(
                (fid, fragment["targets"][0])
                for fid, fragment in synthetic.relation["fragments"].items()
                if fragment.get("targets"))
            target["note"] = adversarial
            target["rationale"] = adversarial

            phrase_fid, phrase = next(
                (fid, fragment["phrases"][0])
                for fid, fragment in synthetic.relation["fragments"].items()
                if fragment.get("phrases"))
            phrase_unit = synthetic.units[phrase_fid]
            original_phrase = phrase["text"]
            self.assertEqual(phrase_unit.text.count(original_phrase), 1)
            phrase_unit.text = phrase_unit.text.replace(
                original_phrase, adversarial, 1)
            phrase_unit.canonical = canon.canon_prose(phrase_unit.text)
            phrase_unit.digest = canon.text_digest(phrase_unit.canonical)
            phrase["text"] = adversarial

            source_blocks = []
            for fragment in synthetic.relation["fragments"].values():
                if fragment.get("caution", {}).get("source"):
                    source_blocks.append(
                        fragment["caution"]["source"]["block"])
                for target_item in fragment.get("targets", []):
                    if target_item.get("caution", {}).get("source"):
                        source_blocks.append(
                            target_item["caution"]["source"]["block"])
                for phrase_item in fragment.get("phrases", []):
                    if phrase_item.get("caution", {}).get("source"):
                        source_blocks.append(
                            phrase_item["caution"]["source"]["block"])
                    for target_item in phrase_item.get("targets", []):
                        if target_item.get("caution", {}).get("source"):
                            source_blocks.append(
                                target_item["caution"]["source"]["block"])
            for assignments in synthetic.relation["claimGates"].values():
                for assignment in assignments:
                    if assignment.get("source"):
                        source_blocks.append(assignment["source"]["block"])
            self.assertTrue(source_blocks, ed)
            source_block = source_blocks[0]
            synthetic.guidance_anchors = copy.deepcopy(
                base.guidance_anchors)
            synthetic.guidance_anchors[source_block].block.canonical = \
                adversarial

            for mode in ("candidate", "preview"):
                html = render.render(synthetic, mode=mode).decode("utf-8")
                for payload in payloads:
                    self.assertNotIn(payload, html, (ed, mode, payload))

                json_scripts = re.findall(
                    r'<script type="application/json" id="[^"]+">'
                    r'(.*?)</script>', html, re.S)
                self.assertEqual(len(json_scripts), 3)
                for script_blob in json_scripts:
                    canon.parse_json(script_blob)
                    self.assertNotIn("</script", script_blob.lower())

                nav_blob = re.search(
                    r'<script type="application/json" id="nav-data">'
                    r'(.*?)</script>', html, re.S).group(1)
                nav_data = canon.parse_json(nav_blob)
                rendered_target = next(
                    item for item in
                    nav_data["fragments"][target_fid]["targets"]
                    if item["block"] == target["block"])
                self.assertEqual(rendered_target["note"], adversarial)
                self.assertNotIn("rationale", rendered_target)
                rendered_phrase = next(
                    item for item in
                    nav_data["fragments"][phrase_fid]["phrases"]
                    if item["id"] == phrase["id"])
                self.assertEqual(rendered_phrase["text"], adversarial)
                self.assertEqual(
                    nav_data["quotes"][source_block], adversarial)

                static = _without_scripts(html)
                self.assertGreaterEqual(
                    static.count(render.esc(adversarial)), 3,
                    "%s %s did not render note, rationale, and phrase text" %
                    (ed, mode))
                self.assertIn(
                    "quote.textContent = DATA.quotes[caution.source.block]",
                    html)

        # Current artifacts likewise contain no raw fixture payload.
        for ed in EDITIONS:
            html = get_html(ed).decode("utf-8")
            for payload in payloads:
                self.assertNotIn(payload, html)

    def test_ac10_navigation(self):
        for ed in EDITIONS:
            m = get_model(ed)
            html = get_html(ed).decode("utf-8")
            ship = projections.ship_relation(m, "artifact")
            reverse = projections.reverse_index(ship)
            ids = set(re.findall(r'id="([^"]+)"', html))
            # every unit and phrase has its button; statuses render
            for fid, frag in ship["fragments"].items():
                self.assertIn("btn-" + fid, ids)
                for ph in frag.get("phrases", []):
                    self.assertIn("btn-" + ph["id"], ids)
            # every recorded target block resolves in the DOM
            for frag in ship["fragments"].values():
                for t in frag.get("targets", []):
                    self.assertIn(t["block"], ids)
            # badges: one per indexed block, count = fragment count
            badges = dict(re.findall(
                r'class="rev-badge" data-block="([^"]+)"[^>]*>◂ (\d+)<', html))
            self.assertEqual(set(badges), set(reverse))
            for block, n in badges.items():
                self.assertEqual(int(n), len(reverse[block]))
            # claim-level gate chips render at claim headers
            n_gates = sum(len(v) for v in ship.get("claimGates", {}).values())
            self.assertEqual(html.count('class="gate-chip"'), n_gates)
            # mode labels + navbar containers
            for tok in ('id="forward-bar"', 'id="reverse-bar"'):
                self.assertIn(tok, html)
            # Execute the complete inline runtime from the built candidate,
            # including its DOM event handlers (not a source-module surrogate).
            self._node_check(ed, html)

    def _node_check(self, ed, html):
        result = run_navigation_harness(html)
        self.assertIsNone(result["runtimeError"], ed)
        self.assertEqual(result["fails"], [], ed)
        self.assertGreater(result["coverage"]["units"], 0, ed)
        self.assertGreater(result["coverage"]["phrases"], 0, ed)
        self.assertEqual(result["coverage"]["pointerActivations"], 1, ed)
        self.assertEqual(result["coverage"]["reverseActivations"], 1, ed)
        self.assertEqual(result["coverage"]["gateActivations"], 1, ed)
        self.assertGreaterEqual(result["coverage"]["sourceQuotes"], 2, ed)

        # Mutation guard: the old model-only callback could still pass if all
        # DOM behavior after NAVMODEL vanished.  The full-runtime callback must
        # fail that exact mutation.
        runtime = re.search(r'<script>(.*?)</script>\s*</body>', html,
                            re.S).group(1)
        marker = "/*NAVMODEL-END*/"
        self.assertIn(marker, runtime)
        model_only = runtime[:runtime.index(marker) + len(marker)]
        mutant = run_navigation_harness(html, model_only)
        self.assertIn("runtime click handler missing", mutant["fails"], ed)
        self.assertTrue(any(
            "activation did not show forward bar" in problem
            for problem in mutant["fails"]), mutant)

    def test_ac11_accessibility_static(self):
        na_model = get_model("na")
        preview = self._assert_active_technical_preview(
            na_model.release_policy)
        self.assertIn("AC-11.observed", preview["deferredControls"])
        support = na_model.support_matrix
        expected_targets = [
            {"browser": "Chrome ≥ 126", "os": "macOS 13+", "at": "none",
             "mode": "local file, double-click"},
            {"browser": "Chrome ≥ 126", "os": "Windows 11", "at": "none",
             "mode": "local file, double-click"},
            {"browser": "Edge ≥ 126", "os": "Windows 11", "at": "none",
             "mode": "local file, double-click"},
            {"browser": "Firefox ≥ 128", "os": "macOS 13+", "at": "none",
             "mode": "local file, double-click"},
            {"browser": "Firefox ≥ 128", "os": "Windows 11", "at": "none",
             "mode": "local file, double-click"},
            {"browser": "Safari ≥ 17", "os": "macOS 13+", "at": "none",
             "mode": "local file, double-click"},
            {"browser": "Chrome ≥ 126", "os": "Windows 11",
             "at": "NVDA 2024+", "mode": "local file, double-click"},
        ]
        self.assertEqual(support["supportMatrixVersion"], "2")
        self.assertEqual(support["targets"], expected_targets)
        self.assertNotIn("voiceover",
                         json.dumps(support["targets"]).casefold())
        safari_targets = [target for target in support["targets"]
                          if target["browser"] == "Safari ≥ 17"]
        self.assertEqual(len(safari_targets), 1,
                         "support matrix must have exactly one Safari target")
        self.assertEqual(safari_targets[0], {
            "browser": "Safari ≥ 17",
            "os": "macOS 13+",
            "at": "none",
            "mode": "local file, double-click",
        })
        for ed in EDITIONS:
            html = get_html(ed).decode("utf-8")
            self._assert_preview_artifact_label(html, preview)
            self.assertIn('aria-live="polite"', html)
            self.assertNotIn("<button", re.sub(
                r"<button[^>]*>[^<]*</button>", "", html).replace(
                "</button>", ""))  # no nested interactive controls
            self.assertIn("min-height:24px", html)
            self.assertIn("Escape", html)
            self.assertIn("ArrowLeft", html)
            self.assertIn("prefers-reduced-motion", html)
            for b in re.findall(r"<button[^>]*>", html):
                self.assertTrue("aria-label" in b or "data-goto" in b or
                                "data-aux" in b, b)
        # Live row-by-row browser/OS/AT observations remain part of the
        # validated-release profile.  They are explicitly deferred here and
        # therefore do not authorize a compatibility claim for this preview.

    def test_ac12_print_static(self):
        preview = self._assert_active_technical_preview(
            get_model("na").release_policy)
        self.assertIn("AC-12.observed", preview["deferredControls"])
        for ed in EDITIONS:
            html = get_html(ed).decode("utf-8")
            self._assert_preview_artifact_label(
                html, preview, require_print_footer=True)
            self.assertIn("@media print", html)
            self.assertIn("@page { margin:12mm 10mm; }", html)
            self.assertRegex(
                html,
                r"#content-root \{ display:block; overflow:visible; "
                r"padding-bottom:37mm;[^}]*"
                r"-webkit-box-decoration-break:clone; "
                r"box-decoration-break:clone;")
            self.assertIn(
                "#masthead > .legend,#masthead > .release-profile,\n"
                "  #masthead > .disclaimer { display:none; }",
                html)
            self.assertRegex(
                html,
                r"footer \{ position:fixed; top:auto; bottom:0;[^}]*"
                r"height:35mm;[^}]*overflow:hidden;")
            self.assertNotIn("transform:translateY", html)

    def test_ac13_layout_static(self):
        preview = self._assert_active_technical_preview(
            get_model("na").release_policy)
        self.assertIn("AC-13.observed", preview["deferredControls"])
        for ed in EDITIONS:
            m = get_model(ed)
            html = get_html(ed).decode("utf-8")
            self._assert_preview_artifact_label(html, preview)
            width, height = m.support_matrix["viewport"]["minimum"]
            self.assertTrue(
                m.support_matrix["viewport"]["stackedBelowMinimum"])
            self.assertIn(
                "(max-width:%dpx),(max-height:%dpx)" %
                (width - 1, height - 1), html)
            self.assertIn(render.esc(render.microcopy(
                m.strings["ui"]["viewportNote"],
                width=width, height=height)), html)

    def test_ac14_nojs_static(self):
        preview = self._assert_active_technical_preview(
            get_model("na").release_policy)
        self.assertNotIn("AC-14.observed", preview["deferredControls"])
        ac14 = next(
            criterion for criterion in acceptance.load_registry(ROOT)[
                "criteria"]
            if criterion["id"] == "AC-14")
        self.assertEqual(ac14["enforcedBy"]["qaRecordFields"], [])
        for ed in EDITIONS:
            m = get_model(ed)
            html = get_html(ed).decode("utf-8")
            static = _without_scripts(html)
            self._assert_preview_artifact_label(
                static, preview, require_profile_metadata=False)
            self.assertNotIn("<script", static.lower())

            parser = _StaticSectionParser((
                "claims-pane", "disclosure-pane", "schedule", "about"))
            parser.feed(static)
            section_ids = {
                section: {attrs.get("id") for unused_tag, attrs in elements
                          if attrs.get("id")}
                for section, elements in parser.elements.items()
            }

            # Every claim and unit remains present and readable. Phrase buttons
            # may insert the visible CRR diamond between source-text spans; it
            # is removed only for this verbatim-readability comparison.
            claims_text = " ".join(parser.normalized_text(
                "claims-pane").replace("◇", "").split())
            for claim in m.claims:
                self.assertIn(
                    "claim-%d" % claim.number,
                    section_ids["claims-pane"])
                for unit in claim.units:
                    self.assertIn(
                        "u-" + unit.id, section_ids["claims-pane"])
                    self.assertIn(
                        " ".join(unit.text.split()), claims_text, unit.id)

            # Every disclosure block has its static anchor and visible content;
            # table rows and figure alternatives are checked independently.
            disclosure_text = parser.normalized_text("disclosure-pane")
            disclosure_elements = parser.elements["disclosure-pane"]
            image_alts = {
                attrs.get("alt") for tag, attrs in disclosure_elements
                if tag == "img"
            }

            def inline_visible(value):
                inline_parser = _StaticSectionParser(("inline",))
                inline_parser.feed(
                    '<span id="inline">%s</span>' %
                    render.md_inline(value))
                return inline_parser.normalized_text("inline")

            for block in m.target_blocks:
                self.assertIn(
                    block.id, section_ids["disclosure-pane"], block.id)
                if block.kind == "claim-whole":
                    continue
                if block.kind == "figure":
                    self.assertIn(block.label, image_alts, block.id)
                    continue
                if block.kind == "table":
                    values = list(block.meta.get("header") or [])
                    values.extend(
                        cell for row in block.rows for cell in row["cells"])
                    if block.meta.get("caption"):
                        values.append(block.meta["caption"])
                    for row in block.rows:
                        self.assertIn(
                            "%s.%s" % (block.id, row["id"]),
                            section_ids["disclosure-pane"])
                    visible_values = [inline_visible(value) for value in values]
                elif block.kind == "heading":
                    visible_values = [" ".join(block.text.split())]
                elif block.kind == "code":
                    visible_values = [" ".join(block.canonical.split())]
                else:
                    visible_values = [inline_visible(block.text)]
                for value in visible_values:
                    if value:
                        self.assertIn(value, disclosure_text, block.id)

            ship_schedule = projections.ship_relation(m, "schedule")
            expected_schedule = render._schedule(
                m, ship_schedule, m.strings)
            self.assertIn(expected_schedule, static)
            schedule_text = parser.normalized_text("schedule")
            expected_schedule_rows = sum(
                1 + len(ship_schedule["fragments"][unit.id].get(
                    "phrases", []))
                for claim in m.claims for unit in claim.units)
            expected_schedule_rows += sum(
                len(assignments) for assignments in
                ship_schedule.get("claimGates", {}).values())
            actual_schedule_rows = sum(
                tag == "tr" for tag, unused_attrs in
                parser.elements["schedule"])
            self.assertEqual(
                actual_schedule_rows, expected_schedule_rows + 2)
            for fragment in ship_schedule["fragments"].values():
                for owner in [fragment] + list(fragment.get("phrases", [])):
                    if "text" in owner:
                        self.assertIn(
                            " ".join(owner["text"].split()), schedule_text)
                    for target in owner.get("targets", []):
                        self.assertIn(target["block"], schedule_text)
                        self.assertIn(
                            " ".join(target["note"].split()), schedule_text)
                        if target.get("rationale"):
                            self.assertIn(
                                " ".join(target["rationale"].split()),
                                schedule_text)
                for disposition in fragment.get("dispositions", []):
                    self.assertIn(
                        m.strings["dispositions"][
                            disposition["disposition"]], schedule_text)

            provenance = projections.provenance(m)
            provenance["renderTreeHash"] = projections.render_tree_hash(
                m.gw, m.edition["declaredTransitiveInputs"])
            expected_about = render._provenance_html(
                provenance, m.strings, m.support_matrix)
            self.assertIn(expected_about, static)
            about_text = parser.normalized_text("about")
            for corpus in provenance["corpora"]:
                for value in (corpus["id"], corpus["role"],
                              corpus["version"]):
                    self.assertIn(value, about_text)
                for path, digest in corpus["files"].items():
                    self.assertIn(path, about_text)
                    self.assertIn(digest[:23] + "…", about_text)
            authority_record = provenance["authority"]
            for value in (authority_record["id"],
                          authority_record["version"],
                          authority_record["digest"][:23] + "…"):
                self.assertIn(value, about_text)
            for digest_name in (
                    "relationSetDigest", "gateInventoryDigest",
                    "dependencyMapDigest", "editionConfigDigest",
                    "schemaDigest", "stringsProjectionDigest",
                    "renderTreeHash"):
                if provenance.get(digest_name):
                    self.assertIn(digest_name, about_text)
                    self.assertIn(
                        provenance[digest_name][:23] + "…", about_text)

            disclaimer = m.strings["standingDisclaimer"].replace(
                "{editionVersion}", m.edition["claimSetVersion"])
            self.assertGreaterEqual(static.count(render.esc(disclaimer)), 2)
            self.assertIn("<noscript>", static)

    def test_ac15_api_policy(self):
        preview = self._assert_active_technical_preview(
            get_model("na").release_policy)
        self.assertIn("AC-15.observed", preview["deferredControls"])
        for ed in EDITIONS:
            m = get_model(ed)
            self.assertEqual(
                {api: spec["class"]
                 for api, spec in m.api_policy["apis"].items()},
                render.EXPECTED_API_CLASSES)
            html = get_html(ed).decode("utf-8")
            self._assert_preview_artifact_label(html, preview)
            js = html.split("<script>")[-1].split("</script>")[0]
            probe, page = js.split("})();", 1)
            probe += "})();"
            registered = render.api_probe_instruments(m.api_policy)
            for api, spec in m.api_policy["apis"].items():
                if spec["class"] != "probed":
                    continue
                token = api.split(".")[-1]
                self.assertIn(token, probe,
                              "no instrumentation for probed API %s" % api)
            # page code never uses the enumerated APIs
            for tok in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource",
                        "sendBeacon", "localStorage", "sessionStorage",
                        "indexedDB", "document.cookie", "pushState",
                        "replaceState", "location.assign", "location.replace"):
                self.assertNotIn(tok, page,
                                 "page code references %s" % tok)
            self.assertIn("__apiAttempts", probe)
            self.assertIn("__apiProbeStatus", probe)

            # An empty attempts array is evidence only after every exact
            # registered hook reports a verified installation.  Exercise the
            # real artifact bootstrap, then prove that three formerly silent
            # installation failures stay observable and fail closed.
            api_order = (
                "navigator.sendBeacon", "history.pushState",
                "history.replaceState", "window.localStorage",
                "window.sessionStorage", "indexedDB.open",
                "document.cookie",
            )
            production = run_api_probe_harness(
                probe, registered, "success")
            self.assertIsNone(production["thrown"], production)
            self.assertEqual(production["status"]["expected"],
                             sorted(registered))
            self.assertEqual(sorted(production["status"]["hooks"]),
                             sorted(registered))
            self.assertTrue(production["status"]["ready"], production)
            self.assertEqual(production["before"], [])
            self.assertEqual(production["after"], [
                registered[api] for api in api_order])
            self.assertEqual(production["deltas"], {
                api: [registered[api]] for api in api_order})

            # Production labels intentionally group related APIs.  Repeat
            # with unique per-API markers to prove the exact API→hook wiring,
            # rather than merely one working hook somewhere in each group.
            behavior_policy = {
                api: "probe:" + api for api in sorted(registered)}
            wiring = run_api_probe_harness(
                probe, behavior_policy, "success")
            self.assertIsNone(wiring["thrown"], wiring)
            self.assertEqual(wiring["status"]["expected"],
                             sorted(registered))
            self.assertEqual(sorted(wiring["status"]["hooks"]),
                             sorted(registered))
            self.assertTrue(wiring["status"]["ready"], wiring)
            for api in sorted(registered):
                self.assertEqual(wiring["status"]["hooks"][api], {
                    "status": "installed", "error": None, "detail": None,
                })
            self.assertEqual(wiring["before"], [])
            self.assertEqual(wiring["after"], [
                behavior_policy[api] for api in api_order])
            self.assertEqual(wiring["deltas"], {
                api: [behavior_policy[api]] for api in api_order})

            failures = (
                ("nonwritable-function", "history.pushState", "push",
                 "installation-threw"),
                ("getter-failure", "window.localStorage", "localGet",
                 "installation-threw"),
                ("cookie-failure", "document.cookie", "cookieWrite",
                 "descriptor-not-configurable"),
            )
            for scenario, api, call_counter, expected_error in failures:
                with self.subTest(edition=ed, scenario=scenario):
                    failed = run_api_probe_harness(
                        probe, behavior_policy, scenario)
                    self.assertFalse(failed["status"]["ready"], failed)
                    hook = failed["status"]["hooks"][api]
                    self.assertEqual(set(hook), {
                        "status", "error", "detail"})
                    self.assertEqual(hook["status"], "failed")
                    self.assertEqual(hook["error"], expected_error, failed)
                    if expected_error == "installation-threw":
                        self.assertTrue(hook["detail"], failed)
                    self.assertIn("API probe installation failed",
                                  failed["thrown"])
                    self.assertEqual(failed["before"], [])
                    self.assertEqual(
                        failed["after"], [],
                        "the real API ran unrecorded, so ready=false must "
                        "prevent trusting the empty attempts list")
                    self.assertEqual(failed["deltas"], {api: []})
                    self.assertEqual(failed["calls"][call_counter], 1)

    def test_ac16_determinism(self):
        for ed in EDITIONS:
            m = get_model(ed)
            one = render.render(m, mode="candidate")
            two = render.render(m, mode="candidate")
            self.assertEqual(one, two, "double build not byte-identical")
            # across separate interpreter processes: an in-process double
            # build shares hash seeds and cannot detect seed-dependent
            # ordering (AC-16)
            child = subprocess.run(
                [sys.executable, "-c", """
import sys
sys.path.insert(0, "navigator")
from lib import canon, gateway, model, render
ed = %r
boot = gateway.ContentGateway(".")
allow = canon.parse_json(
    boot.read_text("navigator/editions/" + ed + ".json"))
gw = gateway.ContentGateway(".", allowlist=allow["declaredTransitiveInputs"])
m = model.EditionModel(gw, "navigator/editions/" + ed + ".json")
print(canon.bytes_digest(render.render(m, mode="candidate")))
""" % ed], capture_output=True, text=True, cwd=ROOT, timeout=300)
            self.assertEqual(child.returncode, 0, child.stderr)
            self.assertEqual(child.stdout.strip(), canon.bytes_digest(one),
                             "cross-process double build not byte-identical")
            cpath = candidate_path(m)
            self.assertTrue(os.path.exists(cpath))
            with open(cpath, "rb") as fh:
                candidate_bytes = fh.read()
            self.assertEqual(candidate_bytes, one,
                             "dist candidate differs from derivation")
            lock = m.gw.lock()
            self.assertEqual(inputlock.exact_set_problems(
                lock, m.edition["declaredTransitiveInputs"]), [])
            from lib.currentstate import (  # noqa: E402
                _approval_selection_key, _required_attestation_types,
                approval_evidence_problems, current_authorized_qa_records,
                current_side_digests, qa_input_lock)
            all_qas = read_records("qa-record")
            all_attestations = read_records("attestation")
            self.assertNotIn("reproductionDiagnostics",
                             json.dumps(lock))  # diagnostics excluded
            required_types = _required_attestation_types(m)
            current_sides = current_side_digests(m)
            current_acceptance = acceptance.acceptance_context(
                ROOT, (ed,))
            profile_contract = current_acceptance["releaseProfileContract"]
            profile_fields = acceptance.profile_record_fields(
                profile_contract)
            if ACCEPTANCE_CALLBACK_CONTEXT is not None and \
                    ACCEPTANCE_CALLBACK_CONTEXT.get("kind") == \
                    "release-preflight":
                self.assertEqual(ACCEPTANCE_CALLBACK_CONTEXT, {
                    "kind": "release-preflight",
                    "edition": ed,
                    "candidateDigest": canon.bytes_digest(candidate_bytes),
                    "contentLockDigest": lock["lockDigest"],
                })
                continue
            qa = []
            valid_qa_digests = set()
            current_qa_authorization = None
            if profile_contract["manualQaEvidence"] == "required":
                qa, rejected = current_authorized_qa_records(
                    m, canon.bytes_digest(candidate_bytes), lock, all_qas,
                    all_attestations)
                self.assertTrue(
                    qa, "no complete current authorized-operator QA: %s"
                    % rejected)
                self._assert_authorized_record(
                    min(qa, key=_approval_selection_key)["record"],
                    "%s release-preflight QA" % ed)
                valid_qa_digests = {record["digest"] for record in qa}
                current_qa_authorization = {
                    "qaInputLock": qa_input_lock(
                        m, canon.bytes_digest(candidate_bytes),
                        lock["lockDigest"]),
                    "supportMatrixApprover":
                        m.support_matrix.get("approver"),
                    "supportMatrixTargets": copy.deepcopy(
                        m.support_matrix.get("targets")),
                    "supportMatrixViewport": copy.deepcopy(
                        m.support_matrix.get("viewport")),
                    "apiProbeApis": sorted(render.api_probe_instruments(
                        m.api_policy)),
                }
            rel = []
            for envelope in read_records("release-record"):
                record = envelope.get("record", {})
                if (record.get("edition"), record.get("sealed"),
                        record.get("sealedDigest"), record.get("lockDigest"),
                        record.get("declaredReleaseTimestamp"),
                        record.get("releaseProfile")) != (
                        ed, m.edition["artifactName"],
                        canon.bytes_digest(candidate_bytes),
                        lock["lockDigest"],
                        m.edition["declaredReleaseTimestamp"],
                        current_acceptance["releaseProfile"]):
                    continue
                if profile_contract["manualQaEvidence"] == "deferred" and \
                        record.get("qaRecord") is not None:
                    continue
                if profile_contract["manualQaEvidence"] == "required" and \
                        record.get("qaRecord") not in valid_qa_digests:
                    continue
                if bundlezip.release_chain_problems(
                        envelope, all_qas, all_attestations, required_types,
                        current_sides,
                        approval_evidence_problems,
                        current_acceptance,
                        current_qa_authorization):
                    continue
                rel.append(envelope)
            self.assertTrue(rel, "no release-record seals the current "
                            "candidate bytes for %s" % ed)
            release_envelope = min(rel, key=_approval_selection_key)
            self._assert_authorized_record(
                release_envelope["record"], "%s release authorization" % ed)
            for field, expected in profile_fields.items():
                self.assertEqual(release_envelope["record"][field], expected)
            sealed_name = release_envelope["record"]["sealed"]
            sealed = os.path.join(DIST, sealed_name)
            with open(sealed, "rb") as fh:
                sealed_bytes = fh.read()
            self.assertEqual(sealed_bytes, candidate_bytes,
                             "sealed bytes differ from profile candidate")
            with open(sealed + ".sha256", "rb") as fh:
                checksum = fh.read()
            bundlezip.verify_detached_checksum(
                checksum, sealed_name, canon.bytes_digest(sealed_bytes))

    def test_ac17_disclaimer_legend(self):
        strings = canon.parse_json(gateway.ContentGateway(ROOT).read_text(
            "navigator/strings.json"))
        legend_digest = canon.text_digest(
            canon.canon_prose(strings["counselLegend"]))
        from lib.currentstate import (  # noqa: E402
            _approval_selection_key, attestation_evidence_problems,
            current_side_digests)
        for ed in EDITIONS:
            sides_now = current_side_digests(get_model(ed))
            atts = [a for a in read_records("attestation")
                    if a["record"]["type"] == "legend-approval" and
                    not attestation_evidence_problems(a, sides_now, ed)]
            self.assertTrue(
                atts, "no current authorized-operator legend approval for %s"
                % ed)
            selected = min(atts, key=_approval_selection_key)
            self._assert_authorized_record(
                selected["record"], "%s legend approval" % ed)
            self.assertEqual(selected["record"]["sides"]["legendWording"],
                             legend_digest)
            html = get_html(ed).decode("utf-8")
            self.assertGreaterEqual(
                html.count(render.esc(strings["counselLegend"])), 2)
            self.assertIn("Draft navigation aid generated from claim-set",
                          html)
            static = re.sub(r"<script.*?</script>", "", html, flags=re.S)
            self.assertIn(render.esc(strings["counselLegend"]), static)

    def test_ac18_attestations(self):
        # attestation sufficiency: a CURRENT attestation of each required
        # type exists; superseded ones persist in the append-only store
        atts = read_records("attestation")
        for ed in EDITIONS:
            m = get_model(ed)
            from lib.currentstate import (  # noqa: E402
                _approval_selection_key, attestation_evidence_problems,
                current_side_digests)
            sides_now = current_side_digests(m)

            def current(atype):
                return [a for a in atts
                        if a["record"]["type"] == atype and
                        a["record"].get("edition") in (ed, None) and
                        not attestation_evidence_problems(
                            a, sides_now, ed)]
            priority = current("qa-priority-map")
            self.assertTrue(
                priority, "no current priority-map attestation for %s" % ed)
            self._assert_authorized_record(
                min(priority, key=_approval_selection_key)["record"],
                "%s priority-map attestation" % ed)
            crosswalk = m.edition["qaSources"]["crosswalk"]
            if crosswalk is not None:
                self.assertIsInstance(crosswalk, str)
                crosswalk_atts = current("qa-crosswalk")
                self.assertTrue(
                    crosswalk_atts,
                    "no current crosswalk attestation for %s" % ed)
                self._assert_authorized_record(
                    min(crosswalk_atts,
                        key=_approval_selection_key)["record"],
                    "%s crosswalk attestation" % ed)
            else:
                self.assertIsNone(crosswalk)

    def test_ac19_traceability_meta(self):
        registry = acceptance.validate_registry(canon.parse_json(file_text(
            os.path.join(NAV, "schema", "acceptance.json"))))
        policy = profilepolicy.validate_policy(canon.parse_json(file_text(
            os.path.join(NAV, "schema", "release-policy.json"))))
        self.assertEqual(registry["acceptanceVersion"], "3")
        runner = registry["runner"]
        self.assertEqual(set(runner), {
            "runnerVersion", "editions", "testModules", "fixtures",
            "testScopes", "supportFiles"})
        self.assertEqual(runner["runnerVersion"], "3")
        self.assertNotIn("receiptPhases", registry)
        self.assertNotIn("activeReleaseProfile", runner)
        self.assertNotIn("releaseProfiles", runner)

        profile_id, active_profile = acceptance.release_profile_contract(
            policy, registry)
        self.assertEqual((profile_id, active_profile),
                         ("technical-preview", TECHNICAL_PREVIEW_PROFILE))
        with self.assertRaisesRegex(
                acceptance.AcceptanceError, "not the active release profile"):
            acceptance.release_profile_contract(
                policy, registry, "validated-release")
        active_profile["deferredControls"].clear()
        self.assertEqual(
            acceptance.release_profile_contract(policy, registry)[1],
            TECHNICAL_PREVIEW_PROFILE)
        self.assertEqual(
            acceptance.manual_qa_fields(registry),
            tuple(VALIDATED_RELEASE_PROFILE["requiredQaRecordFields"]))

        # Mandatory controls cannot be deleted or reassigned. New criteria
        # remain structurally possible without a code-locked registry digest.
        mutations = []
        missing = copy.deepcopy(registry)
        missing["criteria"].pop(0)
        mutations.append(missing)
        missing_observation = copy.deepcopy(registry)
        missing_observation["criteria"][10]["enforcedBy"][
            "qaRecordFields"] = []
        mutations.append(missing_observation)
        swapped = copy.deepcopy(registry)
        swapped["criteria"][1]["enforcedBy"]["tests"], \
            swapped["criteria"][2]["enforcedBy"]["tests"] = (
                swapped["criteria"][2]["enforcedBy"]["tests"],
                swapped["criteria"][1]["enforcedBy"]["tests"])
        mutations.append(swapped)
        wrong_runner = copy.deepcopy(registry)
        wrong_runner["runner"]["runnerVersion"] = "2"
        mutations.append(wrong_runner)
        for changed in mutations:
            with self.assertRaises(acceptance.AcceptanceError):
                acceptance.validate_registry(changed)

        extended = copy.deepcopy(registry)
        extended["criteria"].append({
            "id": "AC-21", "applicability": "edition",
            "text": "A future feature has an explicit executable owner.",
            "enforcedBy": {
                "tests": [
                    "test_acceptance.Acceptance.test_ac21_future_feature"],
                "qaRecordFields": [],
            },
        })
        self.assertEqual(acceptance.validate_registry(extended), extended)

        self.assertEqual(runner["editions"], sorted(set(runner["editions"])))
        module_specs = {
            entry["module"]: entry["path"]
            for entry in runner["testModules"]
        }
        self.assertEqual(list(module_specs), sorted(module_specs))
        self.assertEqual(len(module_specs), len(runner["testModules"]))
        modules = {}
        for module_name, path in module_specs.items():
            loaded = importlib.import_module("tests." + module_name)
            self.assertEqual(
                os.path.realpath(loaded.__file__),
                os.path.realpath(os.path.join(ROOT, path)))
            modules[module_name] = loaded
        support_paths = runner["supportFiles"]
        self.assertEqual(support_paths, sorted(set(support_paths)))
        for path in support_paths:
            self.assertTrue(os.path.isfile(os.path.join(ROOT, path)), path)
        fixture_paths = [entry["path"] for entry in runner["fixtures"]]
        self.assertEqual(fixture_paths, sorted(set(fixture_paths)))
        selected_editions = set(EDITIONS)
        active_fixtures = {
            entry["path"] for entry in runner["fixtures"]
            if not entry["editions"] or
            selected_editions.intersection(entry["editions"])
        }
        for path in active_fixtures:
            self.assertTrue(os.path.isfile(os.path.join(ROOT, path)), path)

        observed_fields = {
            "AC-11": ["ac11"],
            "AC-12": ["ac12"],
            "AC-13": ["ac13"],
            "AC-15": ["ac15"],
        }
        registered_tests = set()
        for crit in registry["criteria"]:
            enforced = crit["enforcedBy"]
            self.assertTrue(enforced["tests"] or enforced["qaRecordFields"],
                            crit["id"])
            self.assertEqual(
                enforced["qaRecordFields"],
                observed_fields.get(crit["id"], []),
                "%s validated-release QA requirements drifted" %
                crit["id"])
            for tname in enforced["tests"]:
                parts = tname.split(".")
                self.assertEqual(len(parts), 3, tname)
                module_name, class_name, method_name = parts
                self.assertIn(module_name, modules)
                test_class = getattr(modules[module_name], class_name, None)
                self.assertIsInstance(test_class, type, tname)
                self.assertTrue(issubclass(test_class, unittest.TestCase),
                                tname)
                self.assertTrue(hasattr(test_class, method_name),
                                "%s: registered test %s does not exist"
                                % (crit["id"], tname))
                if module_name == "test_acceptance":
                    expected_prefix = "test_%s_" % \
                        crit["id"].lower().replace("-", "")
                    self.assertEqual(class_name, "Acceptance", tname)
                    self.assertTrue(method_name.startswith(expected_prefix),
                                    tname)
                elif module_name == "test_canon":
                    self.assertEqual(crit["id"], "AC-07", tname)
                registered_tests.add(tname)
        self.assertEqual(
            sorted(field for fields in observed_fields.values()
                   for field in fields),
            VALIDATED_RELEASE_PROFILE["requiredQaRecordFields"])
        # reverse direction: every acceptance-designated test and every
        # golden/property canonicalization test maps back to the registry.
        for name in dir(Acceptance):
            if re.match(r"test_ac\d\d_", name):
                full = "test_acceptance.Acceptance.%s" % name
                self.assertIn(full, registered_tests,
                              "%s not registered in acceptance.json" % name)
        canon_module = modules["test_canon"]
        for class_name in ("TestProperties", "TestVectors"):
            test_class = getattr(canon_module, class_name)
            for name in dir(test_class):
                if name.startswith("test_"):
                    full = "test_canon.%s.%s" % (class_name, name)
                    self.assertIn(
                        full, registered_tests,
                        "%s not registered in acceptance.json" % full)
        self.assertEqual(
            {name.split(".", 1)[0] for name in registered_tests},
            set(module_specs))
        scoped_tests = [entry["test"] for entry in runner["testScopes"]]
        self.assertEqual(scoped_tests, sorted(set(scoped_tests)))
        for entry in runner["testScopes"]:
            self.assertIn(entry["test"], registered_tests)
            self.assertTrue(entry["editions"])
            self.assertEqual(entry["editions"],
                             sorted(set(entry["editions"])))
            self.assertEqual(set(entry["editions"]) -
                             set(runner["editions"]), set())

        shared_runner_paths = set(
            runner["supportFiles"] + list(module_specs.values()) +
            list(control_inventory.CONTROL_SOURCE_PATHS))
        for ed in EDITIONS:
            context = acceptance.acceptance_context(ROOT, (ed,))
            locked = {entry["path"] for entry in context["runnerInputs"]}
            expected_fixtures = {
                entry["path"] for entry in runner["fixtures"]
                if not entry["editions"] or ed in entry["editions"]
            }
            self.assertEqual(
                shared_runner_paths | expected_fixtures,
                locked.intersection(
                    shared_runner_paths | set(fixture_paths)))
            self.assertEqual(context["runnerEditions"], [ed])
        ids = [c["id"] for c in registry["criteria"]]
        self.assertTrue(set(acceptance.MINIMUM_CRITERIA).issubset(ids))
        plan = acceptance.control_plan(registry)
        self.assertEqual(set(plan), {
            "release-preflight", "release-postcondition",
            "bundle-postcondition"})
        self.assertIn("AC-16.release-preflight",
                      plan["release-preflight"])
        self.assertIn("AC-16.release-postcondition",
                      plan["release-postcondition"])
        self.assertEqual(plan["bundle-postcondition"], [
            "AC-20.automated", "AC-20.bundle-postcondition"])
        # §14 must match the registry (comparison test, guardrail 17)
        tdd = file_text(TDD)
        sec = tdd[tdd.index("## 14. Acceptance criteria"):]
        sec = sec[:sec.index("## 15.")]

        def norm(t):
            t = re.sub(r"[*`§]", "", t)
            return re.sub(r"\s+", " ", t).strip()
        documented = {}
        for match in re.finditer(
                r"^\d+\. \*\*(AC-\d\d)\*\* (.*?)"
                r"(?=^\d+\. \*\*AC-|^\*\*Shared)", sec, re.M | re.S):
            documented[match.group(1)] = norm(match.group(2))
        shared = re.search(
            r"^\*\*Shared\*\* — \*\*(AC-19)\*\* (.*?)"
            r"(?=^\*\*Bundle)", sec, re.M | re.S)
        bundle = re.search(
            r"^\*\*Bundle\*\* — \*\*(AC-20)\*\* (.*)$",
            sec, re.M | re.S)
        self.assertIsNotNone(shared)
        self.assertIsNotNone(bundle)
        documented[shared.group(1)] = norm(shared.group(2))
        documented[bundle.group(1)] = norm(bundle.group(2))
        self.assertEqual(set(documented),
                         {criterion["id"] for criterion in registry["criteria"]})
        for criterion in registry["criteria"]:
            self.assertEqual(
                documented[criterion["id"]], norm(criterion["text"]),
                "%s text drifted between §14 and acceptance.json"
                % criterion["id"])

    def _assert_ac20_transaction(self, transaction):
        self.assertIsInstance(transaction, dict)
        self.assertEqual(set(transaction), {
            "kind", "outputRoot", "config", "bundleConfigDigest",
            "bundleDigest", "bundleChecksumDigest", "manifestDigest",
            "plannedMembers", "releaseRecords", "manifestApproval",
            "chain",
        })
        self.assertEqual(transaction["kind"], "bundle-postcondition")
        cfg = transaction["config"]
        self.assertIsInstance(cfg, dict)
        bundlezip.validate_bundle_config(
            cfg, expected_edition_count=len(cfg.get("editions", [])))
        for field in (
                "bundleConfigDigest", "bundleDigest",
                "bundleChecksumDigest", "manifestDigest",
                "manifestApproval"):
            canon.parse_digest(transaction[field])

        planned = transaction["plannedMembers"]
        self.assertEqual(
            planned,
            [{"name": member["name"], "digest": member["digest"]}
             for member in cfg["members"]])
        self.assertEqual(
            transaction["releaseRecords"],
            [member["releaseRecord"] for member in cfg["members"]
             if member["kind"] == "sealed"])
        self.assertEqual(
            transaction["manifestApproval"], cfg["manifestApproval"])

        output_root = transaction["outputRoot"]
        self.assertIsInstance(output_root, str)
        self.assertTrue(os.path.isabs(output_root))
        output_root = os.path.realpath(output_root)

        def output_bytes(name):
            path = os.path.realpath(os.path.join(output_root, name))
            self.assertEqual(os.path.commonpath((output_root, path)),
                             output_root)
            with open(path, "rb") as fh:
                return fh.read()

        bundle_bytes = output_bytes(cfg["name"])
        checksum_bytes = output_bytes(cfg["name"] + ".sha256")
        manifest_member = next(
            member for member in cfg["members"]
            if member["kind"] == "bundle-manifest")
        manifest_bytes = output_bytes(manifest_member["name"])
        self.assertEqual(canon.bytes_digest(bundle_bytes),
                         transaction["bundleDigest"])
        self.assertEqual(canon.bytes_digest(checksum_bytes),
                         transaction["bundleChecksumDigest"])
        self.assertEqual(canon.bytes_digest(manifest_bytes),
                         transaction["manifestDigest"])
        bundlezip.verify_detached_checksum(
            checksum_bytes, cfg["name"], transaction["bundleDigest"])

        members = bundlezip.read_zip_members(bundle_bytes)
        self.assertEqual(
            [{"name": name, "digest": canon.bytes_digest(data)}
             for name, data in members], planned)
        self.assertEqual(
            bundlezip.build_zip(members, cfg["declaredTimestamp"]),
            bundle_bytes)
        self.assertEqual(dict(members)[manifest_member["name"]],
                         manifest_bytes)
        self.assertTrue(manifest_bytes.endswith(b"\n"))
        self.assertFalse(manifest_bytes.endswith(b"\n\n"))
        manifest_text = manifest_bytes[:-1].decode("utf-8")
        self.assertNotIn("sha256/c1:", manifest_text)
        self.assertEqual(
            canon.text_digest(canon.canon_prose(manifest_text)),
            manifest_member["wordingDigest"])

        chain = transaction["chain"]
        self.assertIsInstance(chain, dict)
        self.assertEqual(set(chain), {
            "releaseRecords", "qaRecords", "attestations",
            "requiredAttestationsByEdition", "currentSidesByEdition",
            "acceptanceContextByEdition",
            "qaAuthorizationContextByEdition",
            "currentReleaseBindingsByEdition",
        })
        editions = set(cfg["editions"])
        for field in (
                "requiredAttestationsByEdition", "currentSidesByEdition",
                "acceptanceContextByEdition",
                "qaAuthorizationContextByEdition",
                "currentReleaseBindingsByEdition"):
            self.assertIsInstance(chain[field], dict)
            self.assertEqual(set(chain[field]), editions)
        required = {}
        for edition in cfg["editions"]:
            values = chain["requiredAttestationsByEdition"][edition]
            self.assertIsInstance(values, list)
            self.assertEqual(values, sorted(set(values)))
            self.assertTrue(values)
            required[edition] = frozenset(values)

        from lib.currentstate import approval_evidence_problems  # noqa: E402

        resolved = bundlezip.resolve_bundle_members(
            cfg, chain["releaseRecords"], chain["qaRecords"],
            chain["attestations"],
            lambda unused_kind, name: output_bytes(name),
            manifest_bytes, manifest_member["wordingDigest"],
            approval_evidence_problems, required,
            chain["currentSidesByEdition"],
            expected_edition_count=len(cfg["editions"]),
            acceptance_context_by_edition=
                chain["acceptanceContextByEdition"],
            qa_authorization_context_by_edition=
                chain["qaAuthorizationContextByEdition"])
        self.assertEqual(resolved["members"], members)
        self.assertEqual(resolved["releaseRecords"],
                         transaction["releaseRecords"])
        self.assertEqual(resolved["manifestApproval"],
                         transaction["manifestApproval"])

        release_by_digest = {
            envelope.get("digest"): envelope
            for envelope in chain["releaseRecords"]
            if isinstance(envelope, dict)
        }
        qa_by_digest = {
            envelope.get("digest"): envelope
            for envelope in chain["qaRecords"]
            if isinstance(envelope, dict)
        }
        attestation_by_digest = {
            envelope.get("digest"): envelope
            for envelope in chain["attestations"]
            if isinstance(envelope, dict)
        }
        profile_contract = chain["acceptanceContextByEdition"][
            cfg["editions"][0]]["releaseProfileContract"]
        profile_fields = acceptance.profile_record_fields(profile_contract)
        self.assertTrue(manifest_text.startswith(
            profile_contract["artifactLabel"]))
        for member in cfg["members"]:
            if member["kind"] != "sealed":
                continue
            record = release_by_digest[member["releaseRecord"]]["record"]
            self._assert_authorized_record(
                record, "%s resolved release" % member["edition"])
            for field, expected in profile_fields.items():
                self.assertEqual(record[field], expected)
            if profile_contract["manualQaEvidence"] == "deferred":
                self.assertIsNone(record["qaRecord"])
            else:
                qa_record = qa_by_digest[record["qaRecord"]]["record"]
                self._assert_authorized_record(
                    qa_record, "%s resolved QA" % member["edition"])
                self.assertEqual(qa_record["releaseProfile"],
                                 cfg["releaseProfile"])
            for digest in record["attestations"]:
                self._assert_authorized_record(
                    attestation_by_digest[digest]["record"],
                    "%s resolved attestation %s" %
                    (member["edition"], digest))
            self.assertEqual(
                chain["currentReleaseBindingsByEdition"][member["edition"]],
                {
                    "sealed": record["sealed"],
                    "sealedDigest": record["sealedDigest"],
                    "lockDigest": record["lockDigest"],
                    "declaredReleaseTimestamp":
                        record["declaredReleaseTimestamp"],
                })
        manifest_approval = attestation_by_digest[
            transaction["manifestApproval"]]["record"]
        self._assert_authorized_record(
            manifest_approval, "resolved manifest approval")

        golden = fixture("golden_bundle.json")
        golden_bytes = bundlezip.build_zip(
            [(name, data.encode("ascii"))
             for name, data in golden["members"]],
            golden["declaredTimestamp"])
        self.assertEqual(golden_bytes.hex(), golden["hex"])
        self.assertEqual(canon.bytes_digest(golden_bytes), golden["sha256"])

    def test_ac20_bundle(self):
        if ACCEPTANCE_CALLBACK_CONTEXT is not None:
            self._assert_ac20_transaction(ACCEPTANCE_CALLBACK_CONTEXT)
            return
        from lib.currentstate import (  # noqa: E402
            _approval_selection_key, _propose_current_bundle_config,
            approval_evidence_problems, bundle_acceptance_context,
            bundle_attestation_context, bundle_qa_authorization_context,
            current_release_bindings)
        config_rel = "navigator/bundles/na-af-2026.json"
        boot = gateway.ContentGateway(ROOT)
        cfg = canon.parse_json(boot.read_text(config_rel))
        bundlezip.validate_bundle_config(cfg)
        acceptance_contexts = bundle_acceptance_context(cfg)
        bundle_receipt_context = acceptance.combine_acceptance_contexts(
            acceptance_contexts, cfg["editions"])
        bpath = os.path.join(DIST, cfg["name"])
        self.assertTrue(os.path.exists(bpath), "bundle not built")
        with open(bpath, "rb") as fh:
            zip_bytes = fh.read()
        bundle_digest = canon.bytes_digest(zip_bytes)
        recs = [r for r in read_records("bundle-record")
                if r.get("record", {}).get("bundleDigest") == bundle_digest]
        self.assertTrue(recs, "no bundle-record for the current bundle bytes")
        eligible = []
        rejected = []
        for envelope in recs:
            problems = bundlezip.bundle_record_problems(
                envelope["record"], cfg, bundle_digest,
                boot.read_log[config_rel],
                current_acceptance_context=bundle_receipt_context)
            if problems:
                rejected.extend(problems)
            else:
                eligible.append(envelope)
        self.assertTrue(
            eligible,
            "no current authorized bundle-record for the current bundle "
            "bytes: %s" % ("; ".join(sorted(set(rejected))) or
                            "no eligible record"))
        rec = min(eligible, key=_approval_selection_key)["record"]
        self._assert_authorized_record(rec, "bundle authorization")
        self.assertEqual(bundlezip.bundle_record_problems(
            rec, cfg, bundle_digest,
            boot.read_log[config_rel],
            current_acceptance_context=bundle_receipt_context), [])
        with zipfile.ZipFile(bpath) as zf:
            names = zf.namelist()
            expected = [member["name"] for member in cfg["members"]]
            self.assertEqual(names, expected)
            for info, configured in zip(zf.infolist(), cfg["members"]):
                self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                data = zf.read(info.filename)
                self.assertEqual(configured["digest"],
                                 canon.bytes_digest(data))
                member = [x for x in rec["members"]
                          if x["name"] == info.filename]
                self.assertEqual(member[0]["digest"],
                                 canon.bytes_digest(data))
            manifest_member = next(
                member for member in cfg["members"]
                if member["kind"] == "bundle-manifest")
            manifest = zf.read(manifest_member["name"]).decode("utf-8")
        self.assertEqual(
            rec["releaseRecords"],
            [member["releaseRecord"] for member in cfg["members"]
             if member["kind"] == "sealed"])
        all_releases = read_records("release-record")
        all_qas = read_records("qa-record")
        all_attestations = read_records("attestation")
        bindings = current_release_bindings(cfg)
        qa_authorization_contexts = bundle_qa_authorization_context(
            cfg, bindings)
        attestation_policy, current_attestation_sides = \
            bundle_attestation_context(cfg)
        for release_digest in rec["releaseRecords"]:
            matching = [envelope for envelope in all_releases
                        if envelope["digest"] == release_digest]
            self.assertEqual(
                len(matching), 1,
                "configured bundle release must resolve exactly")
            release_record = matching[0]["record"]
            edition = release_record["edition"]
            self._assert_authorized_record(
                release_record, "%s configured release" % edition)
            self.assertEqual({
                "sealed": release_record["sealed"],
                "sealedDigest": release_record["sealedDigest"],
                "lockDigest": release_record["lockDigest"],
                "declaredReleaseTimestamp":
                    release_record["declaredReleaseTimestamp"],
            }, bindings[edition],
                "configured release is not independently current for %s"
                % edition)
            self.assertEqual(
                bundlezip.release_chain_problems(
                    matching[0], all_qas, all_attestations,
                    attestation_policy[matching[0]["record"]["edition"]],
                    current_attestation_sides[
                        matching[0]["record"]["edition"]],
                    approval_evidence_problems,
                    acceptance_contexts[
                        matching[0]["record"]["edition"]],
                    qa_authorization_contexts[
                        matching[0]["record"]["edition"]]),
                [], "bundle release lacks a complete authorized-operator "
                "QA chain")
        manifest_resource = canon.parse_json(boot.read_text(
            "navigator/bundle-manifest.json"))
        manifest_bytes = (manifest_resource["bundleManifestText"] + "\n").encode(
            "utf-8")
        manifest_wording = canon.text_digest(
            canon.canon_prose(manifest_resource["bundleManifestText"]))
        planes = canon.parse_json(boot.read_text("navigator/schema/planes.json"))
        artifacts = gateway.ArtifactGateway(DIST, "bundle", planes)
        plan = bundlezip.resolve_bundle_members(
            cfg, all_releases, all_qas, all_attestations, artifacts.read,
            manifest_bytes, manifest_wording, approval_evidence_problems,
            attestation_policy, current_attestation_sides,
            acceptance_context_by_edition=acceptance_contexts,
            qa_authorization_context_by_edition=
                qa_authorization_contexts)
        proposed = _propose_current_bundle_config(
            cfg, all_releases, all_qas, all_attestations, artifacts.read,
            manifest_bytes, manifest_wording, attestation_policy,
            current_attestation_sides, acceptance_contexts, bindings,
            qa_authorization_contexts)
        self.assertEqual(
            proposed, cfg,
            "bundle config differs from the independently current plan")
        self.assertEqual(bundlezip.read_zip_members(zip_bytes),
                         plan["members"])
        self.assertEqual(rec["releaseRecords"], plan["releaseRecords"])
        self.assertEqual(rec["manifestApproval"], plan["manifestApproval"])
        # golden bundle fixture: byte-exact writer conformance
        gold = fixture("golden_bundle.json")
        built = bundlezip.build_zip(
            [(n, d.encode("ascii")) for n, d in gold["members"]],
            gold["declaredTimestamp"])
        self.assertEqual(built.hex(), gold["hex"])
        self.assertEqual(canon.bytes_digest(built), gold["sha256"])
        # detached checksum + neutral manifest wording digest
        with open(bpath + ".sha256", "rb") as fh:
            bundle_checksum = fh.read()
        bundlezip.verify_detached_checksum(
            bundle_checksum, cfg["name"], canon.bytes_digest(zip_bytes))
        manifest_resource = canon.parse_json(boot.read_text(
            "navigator/bundle-manifest.json"))
        want = canon.text_digest(
            canon.canon_prose(manifest_resource["bundleManifestText"]))
        self.assertEqual(rec["manifestWording"], want)
        atts = [a for a in read_records("attestation")
                if a["digest"] == cfg["manifestApproval"] and
                a["record"]["type"] == "manifest-approval"]
        self.assertEqual(len(atts), 1,
                         "configured manifest approval must resolve exactly")
        self.assertEqual(approval_evidence_problems(atts[0]["record"]), [],
                         "manifest approval is not authorized-operator evidence")
        self._assert_authorized_record(
            atts[0]["record"], "configured manifest approval")
        self.assertEqual(atts[0]["record"]["sides"],
                         {"manifestWording": want})
        self.assertEqual(rec["manifestApproval"], atts[0]["digest"])
        self.assertNotIn("sha256/c1:", manifest)  # no verification refs


if __name__ == "__main__":
    unittest.main()
