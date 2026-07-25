<!-- GENERATED REVIEW PROJECTION — source us-prior-art-c8; digest sha256/xc1/ssp-xd1:1138e39c0edf57250962d7cfbecbf27ece05ff45def065b03531e5ff341744cd; source profile pdf-evidence-transcription-v1; projection profile gfm-v1/generated-v1; regenerate with `uv --no-cache --offline run --locked --no-sync python -m structured_source regenerate us-prior-art-c8`; edit the XML source, never this Markdown. -->
<a id="ssp-us-prior-art-c8-root"></a>

<a id="ssp-us-prior-art-c8-header-00001"></a>
# C8 — ETSI TS 104 002 V1.1.1 (2023-08) — DASH-IF Forensic A/B Watermarking

<a id="ssp-us-prior-art-c8-blockquote-00002"></a>
> <a id="ssp-us-prior-art-c8-para-00003"></a>
> **WORKING TRANSCRIPTION — NOT AN OFFICIAL COPY AND NOT FOR FILING.**
>
> <a id="ssp-us-prior-art-c8-para-00004"></a>
> Source: `C8_ETSI-TS-104-002_DASH-IF-AB-Watermarking.pdf`. Working transcription produced with OCR from the stored PDF. Verify every quotation, number, date, and reference numeral against the stored PDF; the co-located source manifest records its current evidence binding.
>
> <a id="ssp-us-prior-art-c8-para-00005"></a>
> Text-layer extraction: characters are the publisher's own, not inferred. Reading order is reconstructed from line geometry, so paragraph flow across page and column breaks — and table alignment — still needs visual confirmation against the PDF. Line-number artifacts (5, 10, 15 …) may remain mid-sentence.

<a id="ssp-us-prior-art-c8-horizontalrule-00006"></a>

---

<a id="ssp-us-prior-art-c8-header-00007"></a>
### Page 1

<a id="ssp-us-prior-art-c8-para-00008"></a>
(2023-08) ETSI TS 104 002 V1.1.1

<a id="ssp-us-prior-art-c8-para-00009"></a>
TECHNICAL SPECIFICATION

<a id="ssp-us-prior-art-c8-codeblock-00010"></a>
```
         Publicly Available Specification (PAS);
        DASH-IF Forensic A/B Watermarking
 An interoperable watermarking integration schema

                                CAUTION

           The present document has been submitted to ETSI as a PAS produced by DASH-IF and
```

<a id="ssp-us-prior-art-c8-para-00011"></a>
approved by the Joint Technical Committee (JTC) Broadcast of the European Broadcasting Union (EBU), Comité Européen de
Normalisation ELECtrotechnique (CENELEC) and the European Telecommunications Standards Institute (ETSI).

<a id="ssp-us-prior-art-c8-para-00012"></a>
DASH-IF is owner of the copyright of the document DASH-IF CPIX and/or had all relevant rights and had assigned said rights to
ETSI on an "as is basis". Consequently, to the fullest extent permitted by law, ETSI disclaims all warranties whether express,
implied, statutory or otherwise including but not limited to merchantability, non-infringement of any intellectual property rights of
third parties. No warranty is given about the accuracy and the completeness of the content of the present document.

<a id="ssp-us-prior-art-c8-horizontalrule-00013"></a>

---

<a id="ssp-us-prior-art-c8-header-00014"></a>
### Page 2

<a id="ssp-us-prior-art-c8-para-00015"></a>
2 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-codeblock-00016"></a>
```
                                             Reference
                                       DTS/JTC-118

                                       Keywords
                             broadband, CDN, DASH, DRM, internet, PAS

                                      ETSI

                                   650 Route des Lucioles
                            F-06921 Sophia Antipolis Cedex - FRANCE

                                      Tel.: +33 4 92 94 42 00  Fax: +33 4 93 65 47 16

                                                    Siret N° 348 623 562 00017 - APE 7112B
                                            Association à but non lucratif enregistrée à la
                                         Sous-Préfecture de Grasse (06) N° w061004871

                                    Important notice

                        The present document can be downloaded from:
                                     https://www.etsi.org/standards-search
```

<a id="ssp-us-prior-art-c8-para-00017"></a>
The present document may be made available in electronic versions and/or in print. The content of any electronic and/or
print versions of the present document shall not be modified without the prior written authorization of ETSI. In case of any
existing or perceived difference in contents between such versions and/or in print, the prevailing version of an ETSI
deliverable is the one made publicly available in PDF format at [www\.etsi\.org/deliver](http://www.etsi.org/deliver).

<a id="ssp-us-prior-art-c8-para-00018"></a>
Users of the present document should be aware that the document may be subject to revision or change of status.
Information on the current status of this and other ETSI documents is available at
[https://portal\.etsi\.org/TB/ETSIDeliverableStatus\.aspx](https://portal.etsi.org/TB/ETSIDeliverableStatus.aspx)

<a id="ssp-us-prior-art-c8-codeblock-00019"></a>
```
            If you find errors in the present document, please send your comment to one of the following services:
                            https://portal.etsi.org/People/CommiteeSupportStaff.aspx

                        If you find a security vulnerability in the present document, please report it through our
                              Coordinated Vulnerability Disclosure Program:
                        https://www.etsi.org/standards/coordinated-vulnerability-disclosure

                         Notice of disclaimer & limitation of liability
```

<a id="ssp-us-prior-art-c8-para-00020"></a>
The information provided in the present deliverable is directed solely to professionals who have the appropriate degree of
experience to understand and interpret its content in accordance with generally accepted engineering or
other professional standard and applicable regulations.
No recommendation as to products and services or vendors is made or should be implied.
No representation or warranty is made that this deliverable is technically accurate or sufficient or conforms to any law
and/or governmental rule and/or regulation and further, no representation or warranty is made of merchantability or fitness
for any particular purpose or against infringement of intellectual property rights.
In no event shall ETSI be held liable for loss of profits or any other incidental or consequential damages.

<a id="ssp-us-prior-art-c8-para-00021"></a>
Any software contained in this deliverable is provided "AS IS" with no warranties, express or implied, including but not
limited to, the warranties of merchantability, fitness for a particular purpose and non-infringement of intellectual property
rights and ETSI shall not be held liable in any event for any damages whatsoever (including, without limitation, damages
for loss of profits, business interruption, loss of information, or any other pecuniary loss) arising out of or related to the use
of or inability to use the software.

<a id="ssp-us-prior-art-c8-codeblock-00022"></a>
```
                                Copyright Notification
```

<a id="ssp-us-prior-art-c8-para-00023"></a>
No part may be reproduced or utilized in any form or by any means, electronic or mechanical, including photocopying and
microfilm except as authorized by written permission of ETSI.
The content of the PDF version shall not be modified without the written authorization of ETSI.
The copyright and the foregoing restriction extend to reproduction in all media.

<a id="ssp-us-prior-art-c8-codeblock-00024"></a>
```
                            © ETSI 2023.
                     © European Broadcasting Union 2023.
                                                         All rights reserved.

                                         ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00025"></a>

---

<a id="ssp-us-prior-art-c8-header-00026"></a>
### Page 3

<a id="ssp-us-prior-art-c8-para-00027"></a>
Contents
2.1
2.2
3.1
3.2
3.3
5.1
5.2
5.3
5.4
5.5
5.5.1
5.5.2
5.5.3
5.5.3.1
5.5.3.2
5.5.3.3
5.5.3.4
5.5.3.5
5.5.3.6
5.6
5.6.1
5.6.2
5.6.3
5.6.4
5.6.4.1
5.6.4.2
5.6.4.3
5.6.5
5.7
5.7.1
5.7.2
5.7.3
5.7.4
5.7.5
5.7.5.1
5.7.5.2
5.7.5.3
5.7.5.4
5.8
Annex A (normative):
A.1
A.2
ETSI TS 104 002 V1.1.1 (2023-08)
Intellectual Property Rights ................................................................................................................................ 5
Foreword ............................................................................................................................................................. 5
Modal verbs terminology .................................................................................................................................... 6
Executive summary ............................................................................................................................................ 6
Scope ........................................................................................................................................................ 7
References ................................................................................................................................................ 7
Normative references ......................................................................................................................................... 7
Informative references ........................................................................................................................................ 7
Definition of terms, symbols and abbreviations ....................................................................................... 8
Terms .................................................................................................................................................................. 8
Symbols .............................................................................................................................................................. 8
Abbreviations ..................................................................................................................................................... 8
OTT Watermarking Using Variants ......................................................................................................... 9
Server-Driven Architecture and Workflows .......................................................................................... 10
Introduction ...................................................................................................................................................... 10
Functional Architecture .................................................................................................................................... 10
System Configuration ....................................................................................................................................... 11
WM Token ....................................................................................................................................................... 12
WMPaceInfo .................................................................................................................................................... 14
Introduction................................................................................................................................................. 14
WMPaceInfo Data ...................................................................................................................................... 14
Conveying WMPaceInfo ............................................................................................................................ 14
Introduction ........................................................................................................................................... 14
Sidecar File ........................................................................................................................................... 15
HTTP Header ........................................................................................................................................ 16
ISOBMFF Box ...................................................................................................................................... 17
SEI Message .......................................................................................................................................... 18
TS Adaptation Field .............................................................................................................................. 18
Content Preparation .......................................................................................................................................... 18
Introduction................................................................................................................................................. 18
Encoding Recommendations ...................................................................................................................... 19
Delivering Content and WMPaceInfo from the Encoder to the Packager .................................................. 19
Segment Ingress Path Structure on the Origin ............................................................................................ 20
Introduction ........................................................................................................................................... 20
Locating the Variants ............................................................................................................................ 20
Locating the Sidecar File ...................................................................................................................... 23
Packaging Recommendations ..................................................................................................................... 24
Content Playback .............................................................................................................................................. 25
Introduction................................................................................................................................................. 25
Dynamic Ad Insertion ................................................................................................................................. 25
WM Token, DASH Manifest and HLS Playlists Acquisition ..................................................................... 26
Initialization Segment Acquisition ............................................................................................................. 27
Media Segments and WMPaceInfo Acquisition ......................................................................................... 27
General Requirements ........................................................................................................................... 27
WMPaceInfo Acquisition ...................................................................................................................... 28
Discrete Files......................................................................................................................................... 28
Byterange .............................................................................................................................................. 31
Monitoring and Watermark Detection .............................................................................................................. 33
Vendor Specific Core API ............................................................................. 34
Introduction ............................................................................................................................................ 34
Edge-Vendor Specific API ..................................................................................................................... 34
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00028"></a>

---

<a id="ssp-us-prior-art-c8-header-00029"></a>
### Page 4

<a id="ssp-us-prior-art-c8-para-00030"></a>
Annex B (informative):
B.1
B.2
B.3
Annex C (normative):
C.1
C.2
C.3
Annex D (informative):
D.1
D.2
D.3
D.4
D.5
Annex E (informative):
ETSI TS 104 002 V1.1.1 (2023-08)
Examples of Workflows ................................................................................. 35
Introduction ............................................................................................................................................ 35
Live Content Flows ................................................................................................................................ 35
VOD Content Flows ............................................................................................................................... 37
Registration Requests .................................................................................... 38
General ................................................................................................................................................... 38
IANA Considerations ............................................................................................................................. 38
MP4RA Registration .............................................................................................................................. 40
Code for Web Sequence Diagram ................................................................ 41
Introduction ............................................................................................................................................ 41
Figure 3 .................................................................................................................................................. 41
Figure 5 .................................................................................................................................................. 41
Figure 6 .................................................................................................................................................. 42
Figure 7 .................................................................................................................................................. 42
Change History .............................................................................................. 44
History .............................................................................................................................................................. 45
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00031"></a>

---

<a id="ssp-us-prior-art-c8-header-00032"></a>
### Page 5

<a id="ssp-us-prior-art-c8-para-00033"></a>
Intellectual Property Rights
Essential patents
IPRs essential or potentially essential to normative deliverables may have been declared to ETSI. The declarations
pertaining to these essential IPRs, if any, are publicly available for
found in ETSI SR 000 314:
ETSI in respect of ETSI standards"
ETSI Web server ([https://ipr\.etsi\.org/](https://ipr.etsi.org/)).
Pursuant to the ETSI Directives including the ETSI IPR Policy, no investigation regarding the essentiality of IPRs,
including IPR searches, has been carried out by ETSI. No guarantee can be given as to the existence of other IPRs not
referenced in ETSI SR 000 314 (or the updates on the ETSI Web server) which are, or may be, or may become,
essential to the present document.
Trademarks
The present document may include trademarks and/or tradenames which are asserted and/or registered by their owners.
ETSI claims no ownership of these except for any which are indicated as being the property of ETSI, and conveys no
right to use or reproduce any trademark and/or tradename. Mention of those trademarks in the present document does
not constitute an endorsement by ETSI of products, services or organizations associated with those trademarks.
DECT™, PLUGTESTS™, UMTS™
Members. 3GPP™and LTE™
Organizational Partners. oneM2M™
oneM2M Partners. GSM®
Foreword
This Technical Specification (TS) has been produced by Joint Technical Committee (JTC) Broadcast of the European
Broadcasting Union (EBU), Comité Européen de Normalisation ELECtrotechnique (CENELEC) and the European
Telecommunications Standards Institute (ETSI).
The present document had initially been prepared by DASH-IF (
agreement.
Comments on the present document may be provided at
NOTE:
60 countries in the European broadcasting area; its headquarters is in Geneva.
European Broadcasting Union
CH-1218 GRAND SACONNEX (Geneva)
Switzerland
Tel:
+41 22 717 21 11
Fax:
+41 22 717 24 81
ETSI TS 104 002 V1.1.1 (2023-08)
ETSI members and non-members, and can be
"Intellectual Property Rights (IPRs); Essential, or potentially Essential, IPRs notified to
, which is available from the ETSI Secretariat. Latest updates are available on the
and the ETSI logo are trademarks of ETSI registered for the benefit of its
are trademarks of ETSI registered for the benefit of its Members and of the 3GPP
logo is a trademark of ETSI registered for the benefit of its Members and of the
and the GSM logo are trademarks registered and owned by the GSM Association.
[http://dashif\.org](http://dashif.org)) and was sent to ETSI under the PAS
[https://github\.com/Dash-Industry-Forum/Watermarking/issues](https://github.com/Dash-Industry-Forum/Watermarking/issues).
The EBU/ETSI JTC Broadcast was established in 1990 to co-ordinate the drafting of standards in the
specific field of broadcasting and related fields. Since 1995 the JTC Broadcast became a tripartite body
by including in the Memorandum of Understanding also CENELEC, which is responsible for the
standardization of radio and television receivers. The EBU is a professional association of broadcasting
organizations whose work includes the co-ordination of its members' activities in the technical, legal,
programme-making and programme-exchange domains. The EBU has active members in about
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00034"></a>

---

<a id="ssp-us-prior-art-c8-header-00035"></a>
### Page 6

<a id="ssp-us-prior-art-c8-para-00036"></a>
6 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00037"></a>
Modal verbs terminology

<a id="ssp-us-prior-art-c8-para-00038"></a>
In the present document "shall", "shall not", "should", "should not", "may", "need not", "will", "will not", "can" and
"cannot" are to be interpreted as described in clause 3.2 of the ETSI Drafting Rules (Verbal forms for the expression of
provisions).

<a id="ssp-us-prior-art-c8-para-00039"></a>
"must" and "must not" are NOT allowed in ETSI deliverables except when used in direct citation.

<a id="ssp-us-prior-art-c8-para-00040"></a>
Executive summary

<a id="ssp-us-prior-art-c8-para-00041"></a>
The present document describes proposed architecture and API for supporting forensic watermarking for Over The Top
(OTT) on content that is delivered in an Adaptive Bit Rate (ABR) format. To the possible extend, the proposed
solutions do not make assumptions on the ABR technology that is being used, it can be for example, DASH or HLS.

<a id="ssp-us-prior-art-c8-para-00042"></a>
While digital watermarking can be used for different use cases, the present document focuses on forensic use cases. In
this context, it is used to define the origin of content leakage. the watermarking technology modifies media content in a
robust and invisible way in order to encode a unique identifier, e.g. a unique session ID. The embedded watermark
provides means to identify where the media content, that has been redistributed without authorization, is coming from.
In other words, the watermark is used to forensically trace the origin of content leakage.

<a id="ssp-us-prior-art-c8-codeblock-00043"></a>
```
                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00044"></a>

---

<a id="ssp-us-prior-art-c8-header-00045"></a>
### Page 7

<a id="ssp-us-prior-art-c8-para-00046"></a>
Scope
The present document specifies DASH-IF Forensic A/B Watermarking.
References
2.1
Normative references
References are either specific (identified by date of publication and/or edition number or version number) or
referenced document (including any amendments) applies.
Referenced documents which are not found to be publicly available in the expected location might be found at
[https://docbox\.etsi\.org/Reference](https://docbox.etsi.org/Reference).
NOTE:
their long-term validity.
The following referenced documents are necessary for the application of the present document.
\[1\]
ISO/IEC 23009-1:2022
(DASH) -- Part 1: Media presentation description and segment formats".
\[2\]
ISO/IEC 13818-1:2019
associated audio information -- Part 1: Systems".
\[3\]
IETF Internet Draft draft-pantos-hls-rfc8216bis-12
R. Pantos.
\[4\]
IETF RFC 8949
December 2020.
\[5\]
IETF RFC 8610
Vigano, C. Bormann, June 2019.".
\[6\]
IETF RFC 8392
Tschofenig. May 2018.
\[7\]
IETF RFC 4648
\[8\]
UHD Forum
\[9\]
IEEE Std 1003.1™ 2018 Edition
\[10\]
DASH-IF registry of watermarking technology vendors IDs
\[11\]
IETF RFC 9053
August 2022.
\[12\]
IANA: "CBOR Web Token (CWT) Claims"
2.2
Informative references
References are either specific (identified by date of publication and/or edition number or version number) or
referenced document (including any amendments) applies.
NOTE:
their long term validity.
ETSI TS 104 002 V1.1.1 (2023-08)
non-specific. For specific references, only the cited version applies. For non-specific references, the latest version of the
While any hyperlinks included in this clause were valid at the time of publication, ETSI cannot guarantee
: "Information technology -- Dynamic adaptive streaming over HTTP
: "Information technology -- Generic coding of moving pictures and
: "HTTP Live Streaming 2nd Edition",
: "Concise Binary Object Representation (CBOR)", C. Bormann, P. Hoffman,
: Concise Data Definition Language (CDDL): A Notational Convention to Express
Concise Binary Object Representation (CBOR) and JSON Data Structures", H. Birkholz, C.
: "CBOR Web Token (CWT)", M. Jones, E. Wahlstroem, S. Erdtman, H.
: "The Base16, Base32, and Base64 Data Encodings", S. Josefsson, October 2006.
: "Watermarking API for Encoder Integration, version 1.0.1", March 2021.
, The Open Group Base Specifications Issue 7, 31 January 2018.
.
: "CBOR Object Signing and Encryption (COSE): Initial Algorithms", J. Schaad,
.
non-specific. For specific references, only the cited version applies. For non-specific references, the latest version of the
While any hyperlinks included in this clause were valid at the time of publication, ETSI cannot guarantee
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00047"></a>

---

<a id="ssp-us-prior-art-c8-header-00048"></a>
### Page 8

<a id="ssp-us-prior-art-c8-para-00049"></a>
The following referenced documents are not necessary for the application of the present document but they assist the
user with regard to a particular subject area.
\[i.1\]
DASH-IF Live Media Ingest Protocol.
\[i.2\]
Web Sequence Diagram.
3.1
Terms
For the purposes of the present document, the following terms apply:
client-driven watermarking:
allowing it to make unique requests for content
NOTE:
The user device embeds a watermarking agent that is integrated with the application.
client-side watermarking:
watermarking of content
NOTE:
server-driven watermarking:
operation than conveying information such as tokens, between servers that are responsible for doing the actual
watermarking of content that is delivered to the user device
sequencing: action of returning a Variant of a segment when it is requested, based on a watermark token
NOTE:
variant: alternative representation of a given segment of a multimedia asset
NOTE:
Typically, a Variant is a pre-watermarked version of the segment.
WaterMark (WM) pattern:
3.2
Symbols
Void.
3.3
Abbreviations
For the purposes of the present document, the following abbreviations apply:
ABR
Adaptive Bit Rate
AES
Advanced Encryption Standard
AF
Adaptation Field
API
Application Programming Interface
AVC
Advanced Video Codec
CBOR
Concise Binary Object Representation
CDDL
Concise Data Definition Language
CDN
Content Delivery Network
CMAF
Common Media Application Format
COSE
CBOR Object Signing and Encryption
CPU
Central Processing Unit
CWT
CBOR Web Token
DAI
Dynamic Ad Insertion
DASH
Dynamic Adaptive Streaming over HTTP
DRM
Digital Rights Management
ETSI TS 104 002 V1.1.1 (2023-08)
Definition of terms, symbols and abbreviations
action of watermarking content when the user device is performing some actions
action of watermarking when the user device is the sole responsible for doing the actual
The user device embeds a watermarking agent that is integrated with the audio-visual rendering engine.
action of watermarking content when the user device is not performing any other
Typically, this action is performed on a CDN edge server and is thus referred to as "edge sequencing".
series of A/B decisions for every segment that is unique per user device
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00050"></a>

---

<a id="ssp-us-prior-art-c8-header-00051"></a>
### Page 9

<a id="ssp-us-prior-art-c8-para-00052"></a>
9 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00053"></a>
ECDH Elliptic Curve Diffie-Hellman
HEVC High Efficiency Video Coding
HLS HTTP Live Streaming
HMAC keyed-Hashing for Message AuthentiCation
HTTP Hypertext Transfer Protocol
IANA Internet Assigned Numbers Authority
IOP InterOPerability
IP Internet Protocol
ISOBMFF ISO Base Media File Format
JITP Just In Time Packager
JSON JavaScript Object Notation
JWT JSON Web Token
MPD Media Presentation Description
NAL Network Abstraction Layer
OTT Over The Top
RIST Reliable Internet Stream Transport
RTMP Real-Time Messaging Protocol
RTP Real Time Protocol
SEI Supplemental Enhancement Information
SRT Secure Reliable Transport
TS Transport Stream
TV TeleVision
UDP User Datagram Protocol
UHD Ultra-High Definition
URI Uniform Resource Identifier
URL Uniform Resource Locator
UUID Universally Unique IDentifier
VOD Video On Demand
WM WaterMark
WMID WaterMark IDentifier
WMT WaterMark Token

<a id="ssp-us-prior-art-c8-para-00054"></a>
4 OTT Watermarking Using Variants

<a id="ssp-us-prior-art-c8-para-00055"></a>
The objective of forensic watermarking is to deliver a unique version of a media asset to the different users consuming
the asset. This is somewhat in opposition with media delivery mechanisms that aim at delivering the same asset to all
users for efficiency purposes. As a result, in the broadcast era, a typical approach was to perform the watermarking
operation at the very last step of the media delivery pipeline, within the end user device e.g. a set-top box. This solution
has the virtue of leaving the whole media delivery pipeline unaltered but raises security and interoperability challenges
when a large variety of devices owned and operated by the end user shall be supported. This is for instance the case
with Over The Top (OTT) media delivery where content is consumed on mobile phones, tablets, laptops, connected
TVs, etc. As a result, new forensic watermarking solutions have gained momentum that do not perform security-
sensitive and complex operations in the end user realm. While such approaches require minimal changes in the end-user
devices, they do mandate the media delivery pipeline to be modified accordingly.

<a id="ssp-us-prior-art-c8-para-00056"></a>
A notable example of such network-side watermarking solutions is OTT watermarking using Variants for Adaptive Bit
Rate (ABR) content. In this case, the content is delivered by segments. The baseline idea is then to generate
pre-watermarked Variants of each segment and to modify the delivery protocol so that each end user receives a unique
sequence of Variants depending on a watermark pattern that has been assigned to the end user. The semantic of this
pattern is context dependent and can be, for instance, a device identifier, an account identifier, a session identifier, etc.
Figure 1 illustrates a particular case of this strategy, coined as A/B watermarking, where there are two Variants
generated for each segment, each Variant containing a watermark that either encodes the information '0' or '1'. As a
result, the watermarking system will require the transmission of a sequence of Variants as long as the length of the
pattern to successfully recover the whole unique identifier.

<a id="ssp-us-prior-art-c8-codeblock-00057"></a>
```
                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00058"></a>

---

<a id="ssp-us-prior-art-c8-header-00059"></a>
### Page 10

<a id="ssp-us-prior-art-c8-para-00060"></a>
Ingest
Original asset
ABR segments at different
bitrates
(a)
Ingest
Original asset
A/B Variants of ABR segments at
different bitrates
(b)
When using Variants, the serialization process essentially boils down to delivering a unique sequence of Variants to
each individual end user. There are two main families of methods to achieve this:
1)
2)
sequence of Variants from the CDN.
The present document is describing the server-driven methods. Client-driven methods are not part of the present
document.
Server-Driven Architecture and Workflows
5.1
Introduction
In the server-driven architecture, the device is unaware that content it consumes is watermarked. The device only
exchanges a token with servers allowing these servers, usually CDN edges, to make the decision on which A or B
watermarking metadata that limits the need for naming conventions by allowing the encoder to send this metadata all
the way to the edge through origins to enable the sequencing of bits. The following goes through the functional
architecture and describes the workflows when preparing content and when consuming content.
In the following, it is assumed that the edge is a CDN edge. There are optional architectures, but this does impact the
overall functional architecture and workflows. It is also assumed that multi-track content (audio and video multiplexed
in one segment) is out of the scope of the present document. In addition, all the workflows are only examples of
possible implementations.
5.2
Functional Architecture
Figure
that are involved in the flows when a device consumes watermarked content. Note that this also shows that content is
encrypted, as watermarking will likely be added for premium content that is also encrypted and protected by a DRM
system.
ETSI TS 104 002 V1.1.1 (2023-08)
Alice
Deliver
Bob
Charlie
Sequence of ABR segments
received by three users
Alice
Deliver
Bob
Charlie
Unique sequence of A/B Variants
received by three users
Figure 1: A/B watermarking concept with (a) ABR content delivery and (b) A/B Variants delivery
Server-driven methods, wherein the client does perform no operation related to watermarking. It simply
fetches and forwards a token to the CDN that is responsible for delivering a unique sequence of Variants.
Client-driven methods, wherein the client is responsible for the serialization operation. For instance, it relies
on some session-based digital object to tamper the URI ABR segments and thereby directly query a unique
Variant it delivers to the device. In the present document, an end-to-end system is presented. It includes the definition of
2 shows the simplified high-level functional architecture and the different interaction between the components
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00061"></a>

---

<a id="ssp-us-prior-art-c8-header-00062"></a>
### Page 11

<a id="ssp-us-prior-art-c8-header-00063"></a>
## Content keys & DRM information Authorization DRM Server Server Authz token ; Authz token License To consume content, a device needs, at minimum, to have an authorization token (for getting a DRM license) and a data before requesting segments to the CDN. 5.3 System Configuration Enabling or disabling the edge sequencing logic is set through the configuration to the edge. As an example, this can be useful for a service of live sporting events where only premium events require watermarking enforcement. Other moments of the day do not require it. In this case, content is still watermarked but the edge is only configured to sequence during the limited period of time of the premium event. When sequencing is disabled, the edge shall consume segments on the endpoint for Variant A. If this endpoint is not working properly, the origin shall deliver any available Variant on this endpoint. NOTE 1: When enabling watermarking, all devices that do not have a WM token will receive an error when requesting content, hence they are then forced to request such token. NOTE 2: As an example, enabling and disabling sequencing can be done with an API enable (true/false). Watermarked objects names shall include a pattern that the CDN can match to differentiate these objects from non-watermarked objects (initialization segments, subtitles, trickplay images). As an example, for a DASH manifest located at [https://edge\.hostname/path/to/endpoint/index\.mpd](https://edge.hostname/path/to/endpoint/index.mpd) that references video segments as: `<SegmentTemplate timescale="60000" media="video_segment_$RepresentationID$_$Time$.mp4" initialization="video_init_$RepresentationID$.mp4" startNumber="10967120" presentationTimeOffset="903486496960">` The pattern for the differentiation of these objects from non-watermarked objects is One of the following identification schemes, referred as identification of the Variants:

<a id="ssp-us-prior-art-c8-header-00064"></a>
## A lower-case letter beginning with 'a'. Variants are then 'a', 'b' and so on.

<a id="ssp-us-prior-art-c8-header-00065"></a>
## A number beginning with 0. Variants are then 0, 1 and so on. When addressing content, variantId shall be translated into

<a id="ssp-us-prior-art-c8-para-00066"></a>
variantPath = $\{variantId\}
$\{variantPath\} may be empty.
ETSI TS 104 002 V1.1.1 (2023-08)
Encoder/
Watermarker
A and B Variants
Packager
A and B Variants
Origin
A and B Variants
WMT
Edge
Generator
WM tokens ;
WM token
A or B Variant
Device
Figure 2: Functional architecture
WM token that contains a WM pattern, a series of A or B decisions. The device is responsible for obtaining the required
video\_segment\_.
variantId in the present document, shall be used for the
variantPath as follows:
followed by '/' with the exception, that if $\{variantId\} is 'a' or '0' then
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00067"></a>

---

<a id="ssp-us-prior-art-c8-header-00068"></a>
### Page 12

<a id="ssp-us-prior-art-c8-header-00069"></a>
## 5.4 WM Token A WM token provides a WM pattern which is unique (for example per streaming session or per user). This pattern allows the sequencing of A/B Variants. Two tokenization schemes are defined in the present document. The first, named direct, embeds the WM pattern in the token and can be opened and interpreted by an edge irrespective of the underlying WM technology and provider. The second, named indirect, requires integration of a WM technology provider's edge sequencing software at the edge. The following are requirements on the WM token:

- <a id="ssp-us-prior-art-c8-bulletlist-00070"></a> <a id="ssp-us-prior-art-c8-list-item-00071"></a> <a id="ssp-us-prior-art-c8-empty-list-item-00072"></a>

<a id="ssp-us-prior-art-c8-header-00073"></a>
## clause 4.2.

<a id="ssp-us-prior-art-c8-header-00074"></a>
## Recipients shall process claims listed in IETF RFC 8392 \[6\], clause 3.1 when they are present. shall be present.

<a id="ssp-us-prior-art-c8-header-00075"></a>
## mode). Absence of a wmpattern

<a id="ssp-us-prior-art-c8-header-00076"></a>
## Recipients shall support direct mode and may support indirect mode.

<a id="ssp-us-prior-art-c8-header-00077"></a>
## 256/256 (kty number 5) and ES256 (kty number -7) algorithms.

<a id="ssp-us-prior-art-c8-para-00078"></a>
The token shall be base64url-encoded as described in clause 5 of IETF RFC 4648 \[7\].
The following claims are defined and Table 1 provides the integer claim keys:
wmtoken = \{
wmver-label ^ =\> wmver-value,
wmvnd-label ^ =\> wmvnd-value,
wmpatlen-label ^ =\> wmpatlen-value,
? wmsegduration-label ^ =\> wmsegduration-value,
wmtoken-direct // wmtoken-indirect,

- <a id="ssp-us-prior-art-c8-bulletlist-00079"></a> <a id="ssp-us-prior-art-c8-list-item-00080"></a> <a id="ssp-us-prior-art-c8-plain-00081"></a> wmext-label =\> any
    \}
    wmver-value = uint .size 1
    wmvnd-value = uint .size 1
    wmpatlen-value = uint .size 2
    wmsegduration-value = \[(wmtimeticks : uint, wmtimescale : uint)\]
    wmext-label = int
    ; direct mode
    wmtoken-direct = \{
    wmpattern-label ^ =\> wmpattern-value
    \}
    wmpattern-value = COSE\_Encrypt0 // COSE\_Encrypt // bytes
    ; indirect mode
    wmtoken-indirect = \{
    wmid-label ^ =\> wmid-value
    wmopid-label ^ =\> wmopid-value
    wmkeyver-label ^ =\> wmkeyver-value
    \}
    wmid-value = text
    wmopid-value = uint
    wmkeyver-value = uint
    ETSI TS 104 002 V1.1.1 (2023-08)
    The token shall be a CWT token, the basic structural requirements are defined in IETF RFC 8392 \[6\].
    The token shall be with integer keys in "deterministically encoded CBOR" as specified in IETF RFC 8949 \[4\],
    exp and iat
    The token shall include either a WM pattern (direct mode) or data for deriving the WM pattern (indirect
    claim implies that the token is in indirect mode.
    The token shall be signed as described in clause 7 of IETF RFC 8392 \[6\]. Recipients shall support the HMAC
    ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00082"></a>

---

<a id="ssp-us-prior-art-c8-header-00083"></a>
### Page 13

<a id="ssp-us-prior-art-c8-para-00084"></a>
Claim label
wmver-label
wmvnd-label
wmpatlen-label
wmsegduration-label
wmpattern-label
wmid-label
wmopid-label
wmkeyver-label
wmver
The version of the WM Token. Recipients shall support this claim. The present document describes version 1.
wmvnd
The WM technology vendor. Recipients shall support this claim. This provides the context for the key material needed
for signature verification. In the direct mode, it also provides the context for the key material needed for decrypting
wmpattern
vendor identifiers is available at \[10\].
wmpatlen
The length in bits of the WM pattern. Recipients shall support this claim.
wmpattern
The WM pattern. Recipients shall support this claim in direct mode. It is recommended to encrypt the pattern.
Recipients shall support ECDH-SS+A128KW (key type -32) as defined in IETF RFC 9053 \[11\].
wmsegduration
The nominal duration of a segment. This claim is optional. Recipients may support this claim. When
is not available, this may allow the edge to define the index to be considered in the WM pattern. If
available, this claim shall be ignored. The array contains exactly 2 values. The first value is a duration in time ticks
where its base unit is defined by the second value. The second value is the scale in number of time ticks per second. As
an example, \[60'000, 10'000\] means that the segments are 60'000 ticks long while the scale is 10'000 ticks per second,
wmsegduration is then equal to 6 seconds.
wmid
Used as input to derive the WM pattern for indirect mode. Recipients shall support this claim in indirect mode. The
derivation algorithm is not defined in the present document and is vendor specific.
wmopid
Used as additional input to derive the WM pattern for indirect mode. Recipients shall support this claim in indirect
mode.
wmkeyver
The key to use for derivation of the WM pattern in indirect mode. Recipients shall support this claim in indirect mode.
Once the WM pattern is obtained from the token (either directly, decrypted or calculated), the CDN edge shall enforce
big-endian convention to address a single bit in it when using the value of
The following is an example with a WM pattern equal to
Byte
bit offset
01234567
binary
00001010
hex
0A
For a value of position equal to 3, the bit to consider is
especially, those highlighted in red.
ETSI TS 104 002 V1.1.1 (2023-08)
Table 1: Integer Claim key values for the WM token
Integer key
300
301
302
303
304
305
306
307
if needed. In the indirect mode, it identifies the vendor specific core to use. A list of WM technology
WMPaceInfo data
WMPaceInfo is
position (defined in clause 5.5.2).
0x0A0B0C0D.
01234567
01234567
01234567
00001011
00001100
00001101
0B
0C
0D
highlighted in green (equal to 0). This is not any other bit,
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00085"></a>

---

<a id="ssp-us-prior-art-c8-header-00086"></a>
### Page 14

<a id="ssp-us-prior-art-c8-header-00087"></a>
## For the indirect mode,there is a vendor specific core (identified by on the crypto operations which are used in the direct mode, and its performance should be equivalent. For example, the direct mode relies on one decryption operation when wmpattern consisting of the similar operations to preserve the quantity of operations comparable between these two modes. 5.5 WMPaceInfo 5.5.1 Introduction When a device requests a segment, the edge sequencing logic needs to know which bit in the unique WM pattern to consider for retrieving either A or B Variant of the requested segment before delivering it to the device. combined with the watermarking pre-processor) to the following servers that may need it (packager, origin, or edge). 5.5.2 WMPaceInfo Data WMPaceInfo is as shown in Table 2. Attribute Producer variant Encoder position Encoder firstpart Encoder lastpart Encoder Where

<a id="ssp-us-prior-art-c8-header-00088"></a>
## variant verifying that the right Variant has been obtained.

<a id="ssp-us-prior-art-c8-header-00089"></a>
## position equal to -1, the corresponding segment is not watermarked. For example, segment refers to position 34 of the WM pattern.

<a id="ssp-us-prior-art-c8-header-00090"></a>
## firstpart informs whether this segment is the first one with this the case, otherwise it is equal to false. See clause 5.6.2 for further details.

<a id="ssp-us-prior-art-c8-para-00091"></a>
lastpart informs whether this segment is the last one with this
the case, otherwise it is equal to false. See clause 5.6.2 for further details.
5.5.3
Conveying WMPaceInfo
5.5.3.1
Introduction
WMPaceInfo
document does not recommend one preferred option applicable for all protocols, Table 3 only presents some possible
options for conveying WMPaceInfo
goes through these different options.
ETSI TS 104 002 V1.1.1 (2023-08)
wmvnd). It is recommended that, performance-wise
and software-stack-wise, it is comparable with the direct case. In other words, the vendors specific core should be based
is encrypted, the vendor specific core should be
WMPaceInfo
contains this mapping in addition to some data needed for content preparation. It is transmitted from the encoder (that is
Table 2: WMPaceInfo data
Consumers
Purpose
Edge
Integration, debugging
Edge
Bit position in the WM pattern
Packager, Origin
Egress packaging
Packager, Origin
Egress packaging
gives the Variant identification, 0, 1 and so on. This information can be useful up to the edge for
is the index in the WM pattern to consider for this segment. Positions are zero-based. When it is
position=33 indicates that this
position value. It is equal to true if this is
position value. It is equal to true if this is
is delivered from the encoder to other servers. There is no unique mechanism for this. The present
with a preferred option for some protocols (in bold in the table). The following
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00092"></a>

---

<a id="ssp-us-prior-art-c8-header-00093"></a>
### Page 15

<a id="ssp-us-prior-art-c8-header-00094"></a>
## Ingest protocol RTMP RTP/UDP/RIST/SRT HLS/TS over HTTP POST CMAF-based protocols/formats (HLS/fMP4, DASH) over HTTP POST File access protocol 5.5.3.2 Sidecar File When segments (discrete files or byteranges) are delivered with a file transfer protocol, it may be convenient to have WMPaceInfo data in a sidecar file. For efficiency, the included multiple times. The sidecar file is of the following format (using CDDL representation in IETF RFC 8610 \[5\]), following recommendation of clause 5 of IETF RFC 8949 \[4\] and shall be encoded using deterministically encoded CBOR as specified in IETF RFC 8949 \[4\], clause 4.2 with integer keys. ;---------------------------------------+ ; Maps Integer Keys version = 1 segments = 2 fileSize = 3 startRange = 4 segmentRegex = 5 position = 6 firstpart = 7 lastpart = 8 ;---------------------------------------+ discrete-segment = \{ ?segmentRegex : text, position : int .size 2 .ge -1, ?firstpart : bool, ?lastpart : bool \} byterange-segment = \{ startRange : uint .size 8, position : int .size 2 .ge -1 \} sidecar-discrete = \{ version : uint .size 1, segments : \[+ discrete-segment\] \} sidecar-byterange = \{ version : uint .size 1, fileSize : uint .size 8, segments : \[+ byterange-segment\] \} sidecar = (sidecar-byterange // sidecar-discrete) When segments are discrete files:

<a id="ssp-us-prior-art-c8-header-00095"></a>
## sidecar shall contain only sidecar-discrete

<a id="ssp-us-prior-art-c8-header-00096"></a>
## version is set to 1 for sidecar files compliant to the present document.

<a id="ssp-us-prior-art-c8-header-00097"></a>
## segmentRegex filename of the segments for which the data applies.

<a id="ssp-us-prior-art-c8-para-00098"></a>
position, firstpart and lastpart
ETSI TS 104 002 V1.1.1 (2023-08)
Table 3: Possible options for conveying WMPaceInfo information
WMPaceInfo delivery options
SEI
SEI, TS adaptation field
HTTP header, SEI
HTTP header, ISOBMFF box, SEI
ISOBMFF box, SEI, sidecar file
WMPaceInfo data is not copied directly as some would be
elements.
is a POSIX extended regular expression as described in clause 9 of \[9\]. It allows to define the
segmentRegex is optional.
are defined in clause 5.5.2. firstpart and lastpart are optional.
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00099"></a>

---

<a id="ssp-us-prior-art-c8-header-00100"></a>
### Page 16

<a id="ssp-us-prior-art-c8-header-00101"></a>
## expressions, because of its Central Processing Unit (CPU) load on the origin. The following is an example for a set of segments where the filenames satisfy the example, the filenames are in the form of video\_segment\_\[repID\]*124.mp4 sidecar ( /version/ 1, /segments/ \[\{/segmentRegex/ "video\_segment* .*?*123.mp4", /position/ 21\}, \{/segmentRegex/ "video\_segment* .*?\_124.mp4", /position/ 22\}\] ) When segments are byteranges:

<a id="ssp-us-prior-art-c8-header-00102"></a>
## sidecar shall contain only sidecar-byterange

<a id="ssp-us-prior-art-c8-header-00103"></a>
## version is set to 1 for sidecar files compliant to the present document.

<a id="ssp-us-prior-art-c8-header-00104"></a>
## fileSize is the size of the track in bytes.

<a id="ssp-us-prior-art-c8-header-00105"></a>
## startRange beginning of the track sidecar-byterange startRange values.

<a id="ssp-us-prior-art-c8-para-00106"></a>
position is defined in clause 5.5.2.
NOTE 2: The first byterange of a track contains the initialization segment. When segments are delivered with
therefore position equal -1 for this segment.
The following is an example of a file with an initialization segment part of the byterange from 0 to 1117 and two
segments.
Sidecar (
/version/ 1,
/fileSize/ 262445216,
/segments/ \[\{/startRange/ 0, /position/ -1\},
\{/startRange/ 1118, /position/ 0\},
\{/startRange/ 1701212, /position/ 1\},
…
\{/startRange/ 261083393, /position/ 118\},
\{/startRange/ 262073936, /position/ 119\}\]
)
5.5.3.3
HTTP Header
When content is pushed, in the request header, under the
object is added:
WMPaceInfoIngest : \{
"version": version,
"variant": variant,
"position": position,
"firstpart": firstpart,
"lastpart": lastpart
\}
Where

- <a id="ssp-us-prior-art-c8-bulletlist-00107"></a> <a id="ssp-us-prior-art-c8-list-item-00108"></a> <a id="ssp-us-prior-art-c8-plain-00109"></a> version is set to 1 for WMPaceInfoIngest
    ETSI TS 104 002 V1.1.1 (2023-08)
    NOTE 1: Using regular expressions and file naming conventions allows reducing the number of required side car
    files. The same side car file could be used for all renditions for example. This allows the origin to reduce
    the number of sidecar files, but the edge will always receive several copies of the same data as caching is
    done on the exact filename. It is recommended to balance the advantages and disadvantages of regular
    segmentRegex expression. In this
    video\_segment\_\[repID\]\_123.mp4,
    and so on, allowing to have one sidecar file for all Representations (for DASH).
    elements.
    defines the position of the first byte in the byterange. This expressed as a byte offset from the
    elements in the array shall be ordered in increasing
    byteranges, it is not possible to differentiate the request for this part of the file from a request for a media
    segment when using a pattern as described in clause 5.3. The initialization segment is not watermarked,
    WMPaceInfoIngest HTTP header field, the following JSON
    compliant to the present document.
    ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00110"></a>

---

<a id="ssp-us-prior-art-c8-header-00111"></a>
### Page 17

- <a id="ssp-us-prior-art-c8-bulletlist-00112"></a> <a id="ssp-us-prior-art-c8-list-item-00113"></a> <a id="ssp-us-prior-art-c8-plain-00114"></a> variant, position, firstpart and lastpart
    When content is pulled, in the response header, under the
    CBOR object, base64url-encoded as described in clause 5 of IETF RFC 4648 \[7\], is added:
    WMPaceInfoEgress : `<sidecar-discrete>`
    Where
- <a id="ssp-us-prior-art-c8-list-item-00115"></a> <a id="ssp-us-prior-art-c8-empty-list-item-00116"></a>

<a id="ssp-us-prior-art-c8-para-00117"></a>
sidecar-discrete is defined in clause 5.5.3.2 and contains exactly one
data for that segment.
Below is an example of the JSON element added in a
request contains the full segment of Variant A.
\{
"version": 1,
"variant": 0,
"position": 33,
"firstpart": true,
"lastpart": true
\}
5.5.3.4
ISOBMFF Box
The format of WMPaceInfo class shall be:
class WMPaceInfo \{
unsigned int(8) version;
unsigned int(8) variant;
unsigned int(1) emulation\_1;
unsigned int(15) position;
unsigned int(1) emulation\_2;
unsigned int(1) firstpart;
unsigned int(1) lastpart;
unsigned int(5) reserved;
\}
Where

- <a id="ssp-us-prior-art-c8-bulletlist-00118"></a> <a id="ssp-us-prior-art-c8-list-item-00119"></a> <a id="ssp-us-prior-art-c8-plain-00120"></a> version is set to 1 for WMPaceInfo
- <a id="ssp-us-prior-art-c8-list-item-00121"></a> <a id="ssp-us-prior-art-c8-plain-00122"></a> variant, position, firstpart and lastpart
- <a id="ssp-us-prior-art-c8-list-item-00123"></a> <a id="ssp-us-prior-art-c8-plain-00124"></a> emulation\_1, and emulation\_2 are set to 1.
    Within an ISOBMFF file, the WMPaceInfo
    Box Type:
    'wmpi'
    Container:
    Top level box
    Mandatory: No
    Quantity:
    Zero or one
    aligned(8) class WMPaceInfoBox extends Box('wmpi')
    \{
    WMPaceInfo();
    \}
    This box should be inserted only at the beginning of a segment, after the
    facilitate content manipulation when padding it (see clause 5.7.5.1).
    ETSI TS 104 002 V1.1.1 (2023-08)
    are defined in clause 5.5.2.
    WMPaceInfoEgress HTTP header field, the following
    discrete-segment object with
    WMPaceInfoIngest header field where the payload of the HTTP
    compliant to the present document.
    are defined in clause 5.5.2.
    class shall be carried in the following box:
    styp box and before the moof box, in order to
    ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00125"></a>

---

<a id="ssp-us-prior-art-c8-header-00126"></a>
### Page 18

<a id="ssp-us-prior-art-c8-header-00127"></a>
## 5.5.3.5 SEI Message SEI messages are inserted in the stream with a specific syntax depending on the codec. \[8\] provides the syntax for AVC, HEVC and AV1 video codecs in Annex B. In these messages:

<a id="ssp-us-prior-art-c8-header-00128"></a>
## The UUID shall be equal to

<a id="ssp-us-prior-art-c8-header-00129"></a>
## The watermarking metadata is the WMPaceInfo clause 5.5.3.4. This message should be inserted for the first frame of a segment to facilitate content manipulation when padding it (see clause 5.7.5.1). 5.5.3.6 TS Adaptation Field Following clause U of \[2\], the format of the private adaptation field descriptor carrying the in Table 4. Syntax temi\_WMPaceInfo\_descriptor \{ af\_descr\_tag af\_descr\_length WMPaceInfo() \} Where

<a id="ssp-us-prior-art-c8-header-00130"></a>
## af\_descr\_tag

<a id="ssp-us-prior-art-c8-header-00131"></a>
## af\_descr\_length following af\_descr\_length field.

<a id="ssp-us-prior-art-c8-para-00132"></a>
WMPaceInfo() is a 40-bit field that carries the information defined for the class
clause 5.5.3.4.
This message should be inserted for the first frame of a segment to facilitate content manipulation when padding it (see
clause 5.7.5.1).
5.6
Content Preparation
5.6.1
Introduction
Content preparation means the generation of A/B Variants of the segments followed by the push of content on the
are generated by the packager and pushed to the origin. A simplified flow is shown in Figure 3 for the case of Live
content if the DASH-IF ingest protocol is used \[i.1\] (note that content protection steps are omitted for clarity). For
encrypted content, Variants of every segment part of the same Representation may be encrypted using the same
encryption method and with the same content key, meaning the same DRM license allows decrypting the A and B
Variants. In addition to the Variants, the encoder also pushes
packager and the origin to properly associate the pieces of Variants that are pushed to a bit position on the WM pattern.
ingest segments carrying the same position
ETSI TS 104 002 V1.1.1 (2023-08)
0xbec4f824-170d-47cf-a826-ce008083e355.
data with the format defined for the class WMPaceInfo() in
WMPaceInfo data is defined
Table 4: WMPaceInfo descriptor
No. of bits
Mnemonic
uimsbf
uimsbf
uimsbf
is an 8-bit field that identifies this AF descriptor. It is equal to 0xDF.
is an 8-bit field specifying the number of bytes of the AF descriptor immediately
WMPaceInfo() in
origin. It is under a workflow manager responsibility in case of VOD and fully automated for Live content. The encoder
generates the different Variants of the adaptive content. The encrypted segments, the DASH manifest and HLS playlists
WMPaceInfo that contain information allowing the
In such flow, the packager can aggregate multiple ingest segments into one egress segment, with the limitation that only
value can be aggregated together.
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00133"></a>

---

<a id="ssp-us-prior-art-c8-header-00134"></a>
### Page 19

<a id="ssp-us-prior-art-c8-para-00135"></a>
5.6.2
Encoding Recommendations
This clause contains recommendation when encoding content. The goal is to facilitate the creation and management of
A and B Variants in the delivery chain.
When segments are requested as byteranges in a file or when chunks are requested as byteranges in a segment, the
segments and chunks in A and B Variants shall have the same size as the player receives only one DASH manifest or
HLS playlist and will get byterange lengths from one sidx
present document (as an example, bit stuffing in the encoder is an option).
re-applied over the entire NAL unit after encryption with MPEG-2 TS.
HLS where start code emulation prevention is not re-applied after encryption.
5.6.3
Packager
Only one option for conveying WMPaceInfo
concurrent formats are not allowed.
NOTE 1: When WMPaceInfo
The encoder is sending part of segments to the packager, as the output of the encoder is not necessarily aligned on the
segment length. Furthermore, when multiple streaming formats are used, it may happen that segments generated by the
packager are not of the same size for every streaming protocol (for example, 2 seconds segments for DASH and
4 seconds segments for HLS). The encoder then needs a mechanism for announcing which parts of the Variants it sends
can be aggregated in segments. This is achieved by using the
segments, the encoder ensures that metadata and
For example, the encoder could output the series of content elements of 1 second length with
Figure 4.
ETSI TS 104 002 V1.1.1 (2023-08)
Figure 3: Example of Live DASH content preparation workflow using the DASH-IF ingest protocol
box only. How this is achieved in out of the scope of the
NOTE 1: This solution does not allow creating aligned segment when content is delivered with HLS in the form of
MPEG-2 TS segments encrypted with AES sample encryption, because start code emulation prevention is
NOTE 2: An alternative solution is either to not use segments requested as byteranges, but to use discrete files (in
these cases, there is no need to align Variant A and B of the same segment) or use CMAF segments with
Delivering Content and WMPaceInfo from the Encoder to the
information from the encoder to the origin shall be used. Multiple
is delivered in TS adaptation field, ISOBMFF box, or SEI, it adds overhead in the
delivery from the CDN to devices. The sidecar file and HTTP header delivery methods do not.
firstpart and lastpart within WMPaceInfo.
NOTE 2: Where an encoder delivers additional metadata to instruct the packager how to aggregate the content into
firstpart and lastpart fields are consistent.
WMPaceInfo as shown in
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00136"></a>

---

<a id="ssp-us-prior-art-c8-header-00137"></a>
### Page 20

<a id="ssp-us-prior-art-c8-header-00138"></a>
## 4 seconds 1 second firstpart:0 firstpart:1 firstpart:0 lastpart:0 lastpart:1 lastpart:0 lastpart:0 position:2 position:3 position:3 position:3 If the encoder pushes over HTTP these elements, each one should carry a relevant data. Every server keeps the information within the header associated to the ingested segment. In some cases, for example when the origin does additional packaging, the header may be updated. The packager can then prepare segments according to the streaming protocol. From the example above, it can create segments of 2 or 4 seconds keeping the consistency of the watermarking. NOTE 3: In this case, 2 consecutive segments of 2 seconds carry the same different position values. Other options are to carry WMPaceInfo where the origin can perform additional manipulation of the content, instead providing it is overwritten as specified in clause 5.6.5. 5.6.4 Segment Ingress Path Structure on the Origin 5.6.4.1 Introduction The DASH manifest \[1\] and HLS playlist \[3\] served to the devices are "neutral", meaning that:

<a id="ssp-us-prior-art-c8-header-00139"></a>
## The same playlist or manifest is served to all devices of all end-users.

<a id="ssp-us-prior-art-c8-header-00140"></a>
## It does not expose different names for A and B Variants of a given segment. 5.6.4.2 Locating the Variants Egress DASH manifests and HLS playlists shall be neutral, but ingest DASH manifests and HLS playlists include information about the A and B Variants being ingested, this is:

<a id="ssp-us-prior-art-c8-header-00141"></a>
## The ingest path.

<a id="ssp-us-prior-art-c8-para-00142"></a>
media playlist includes A or B Variants.
The ingest of A and B Variants shall use specific ingest paths that include a Variant identification (
DASH Ingest manifests shall include an AdaptationSet
identical for every Variant apart from an EssentialProperty
Variants are grouped (i.e. they reference the same media). It has the
[http://dashif\.org/guidelines/watermarking\_variant\#$\{variantId\}](http://dashif.org/guidelines/watermarking_variant#%24%7BvariantId%7D)
the Variant with which this EssentialProperty
which the Variant belongs. If there are additional Variants (A, B and C for example), the
different for each Variant, for example, for Variant C,
[http://dashif\.org/guidelines/watermarking\_variant\#c](http://dashif.org/guidelines/watermarking_variant#c)
The following is an example of a DASH ingest manifest with two Variants, A and B. The watermarking signalling is
highlighted in bold. EssentialProperty
("tv1"). In this example, lower case letters are used for
NOTE 1: Segment file naming with template based on segment
`<AdaptationSet mimeType="video/mp4" segmentAlignment="true" startWithSAP="1"
subsegmentAlignment="true" subsegmentStartsWithSAP="1" bitstreamSwitching="true">`
ETSI TS 104 002 V1.1.1 (2023-08)
firstpart:0
firstpart:1
firstpart:0
firstpart:0
lastpart:1
lastpart:0
lastpart:0
position:3
position:4
position:4
Figure 4: Example of output of an encoder
WMPaceInfoIngest HTTP header with the
position value, hence a larger piece of
content is required to retrieve an identifier compared to the case where 2 consecutives segments carrying
in a sidecar file or SEI or ISOBMFF box or TS adaptation field. For cases
WMPaceInfo may be carried within the content
Some signalling elements to describe if a DASH Adaptation Set includes the A or B Variants, or if an HLS
$\{variantId\}).
per Variant. The contents of the AdaptationSet shall be
element that indicates the variantId and that the
@schemeIdUri attribute equal to
where $\{variantId\} identifies
element is associated and @value attribute identifies the group to
@schemeIdUri attribute is
@schemeIdUri attribute shall be equal to
, if the schema with lower case letters is used.
elements indicate that Variant A and Variant B belong to the same group
variantId.
$number or $time are possible.
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00143"></a>

---

<a id="ssp-us-prior-art-c8-header-00144"></a>
### Page 21

<a id="ssp-us-prior-art-c8-para-00145"></a>
`<EssentialProperty schemeIdUri="http://dashif.org/guidelines/watermarking_variant#a"
value="tv1"/>`
`<SegmentTemplate timescale="60000"
media="a/video_segment_$RepresentationID$_$Time$.mp4"
initialization="a/video_init_$RepresentationID$.mp4" startNumber="10967120"
presentationTimeOffset="903486496960">`
`<SegmentTimeline>`
`<S t="903487696960" d="240000"/>`
`<S t="903487936960" d="186000"/>`
`</SegmentTimeline>`
`</SegmentTemplate>`
codecs="avc1.4D4028"/\>
`<Representation id="24" width="1280" height="720" frameRate="30/1" bandwidth="3000000"
codecs="avc1.4D401F"/>`
`<Representation id="26" width="640" height="360" frameRate="30/1" bandwidth="1499968"
codecs="avc1.4D401E"/>`
`</AdaptationSet>`
`<AdaptationSet mimeType="video/mp4" segmentAlignment="true" startWithSAP="1"
subsegmentAlignment="true" subsegmentStartsWithSAP="1" bitstreamSwitching="true">`
`<EssentialProperty schemeIdUri="http://dashif.org/guidelines/watermarking_variant#b"
value="tv1"/>`
`<SegmentTemplate timescale="60000"
media="b/video_segment_$RepresentationID$_$Time$.mp4"
initialization="b/video_init_$RepresentationID$.mp4" startNumber="10967120"
presentationTimeOffset="903486496960">`
`<SegmentTimeline>`
`<S t="903487696960" d="240000"/>`
`<S t="903487936960" d="186000"/>`
`</SegmentTimeline>`
`</SegmentTemplate>`
codecs="avc1.4D4028"/\>
`<Representation id="24" width="1280" height="720" frameRate="30/1" bandwidth="3000000"
codecs="avc1.4D401F"/>`
`<Representation id="26" width="640" height="360" frameRate="30/1" bandwidth="1499968"
codecs="avc1.4D401E"/>`
`</AdaptationSet>`
For HLS ingest playlists, the multivariant playlist shall include all the A and B Variants with a custom attribute
specifying the Variant (using $\{variantId\}
VARIANT
media playlists, the only specific signalling is the segments paths that reflects on which ingest path the Variants are
ingested. The sub-paths in the media playlists shall use the same convention that the
The following is an example of HLS ingest playlists, the watermarking signalling is highlighted in bold (this theoretical
example, both the video and audio are watermarked). In this example, lower case letters are used for
Multivariant playlist
\#EXTM3U
\#EXT-X-VERSION:4
\#EXT-X-INDEPENDENT-SEGMENTS
\#EXT-X-STREAM-INF:BANDWIDTH=5227200,AVERAGE-
BANDWIDTH=3511200,CODECS="avc1.4d401f,mp4a.40.2",RESOLUTION=1280x720,FRAME-
RATE=30.000,AUDIO="program\_audio",
video\_1.m3u8
\#EXT-X-STREAM-INF:BANDWIDTH=2719200,AVERAGE-
BANDWIDTH=1861200,CODECS="avc1.77.30,mp4a.40.2",RESOLUTION=640x360,FRAME-
RATE=30.000,AUDIO="program\_audio",
video\_2.m3u8
\#EXT-X-STREAM-INF:BANDWIDTH=8571200,AVERAGE-
BANDWIDTH=5711200,CODECS="avc1.4d4028,mp4a.40.2",RESOLUTION=1920x1080,FRAME-
RATE=30.000,AUDIO="program\_audio",
video\_3.m3u8
\#EXT-X-STREAM-INF:BANDWIDTH=5227200,AVERAGE-
BANDWIDTH=3511200,CODECS="avc1.4d401f,mp4a.40.2",RESOLUTION=1280x720,FRAME-
RATE=30.000,AUDIO="program\_audio",
video\_4.m3u8
ETSI TS 104 002 V1.1.1 (2023-08)
\<Representation id="27" width="1920" height="1080" frameRate="30/1" bandwidth="5000000"
\<Representation id="27" width="1920" height="1080" frameRate="30/1" bandwidth="5000000"
identification as defined in clause 5.3). The attribute is WATERMARKING-
. A combination of both audio and video watermarking can therefore be used in a single streamset. In the
$\{variantId\}.
variantId.
WATERMARKING-VARIANT="a"
WATERMARKING-VARIANT="a"
WATERMARKING-VARIANT="a"
WATERMARKING-VARIANT="b"
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00146"></a>

---

<a id="ssp-us-prior-art-c8-header-00147"></a>
### Page 22

<a id="ssp-us-prior-art-c8-header-00148"></a>
## \#EXT-X-STREAM-INF:BANDWIDTH=2719200,AVERAGE- BANDWIDTH=1861200,CODECS="avc1.77.30,mp4a.40.2",RESOLUTION=640x360,FRAME- RATE=30.000,AUDIO="program\_audio", video\_5.m3u8 \#EXT-X-STREAM-INF:BANDWIDTH=8571200,AVERAGE- BANDWIDTH=5711200,CODECS="avc1.4d4028,mp4a.40.2",RESOLUTION=1920x1080,FRAME- RATE=30.000,AUDIO="program\_audio", video\_6.m3u8 \#EXT-X-IMAGE-STREAM-INF:BANDWIDTH=55649,AVERAGE- BANDWIDTH=23579,RESOLUTION=308x174,CODECS="jpeg",URI="trickplay\_7.m3u8" \#EXT-X-MEDIA:TYPE=AUDIO,LANGUAGE="eng",NAME="Stadium ambiance",AUTOSELECT=YES,DEFAULT=YES,GROUP- ID="program\_audio",URI="audio\_8.m3u8", \#EXT-X-MEDIA:TYPE=AUDIO,LANGUAGE="eng",NAME="Stadium ambiance",AUTOSELECT=YES,DEFAULT=YES,GROUP- ID="program\_audio",URI="audio\_9.m3u8", NOTE 2: While it is a legal signalling in HLS to have multiple each tag has a different NAME processing on the playlists, the ingest playlists do not follow this rule and multiple the same NAME value. Media playlist (A Variant) \#EXTM3U \#EXT-X-VERSION:6 \#EXT-X-INDEPENDENT-SEGMENTS \#EXT-X-TARGETDURATION:6 \#EXT-X-MEDIA-SEQUENCE:11352692 \#EXT-X-MAP:URI="video\_init\_1.mp4" \#EXT-X-PROGRAM-DATE-TIME:2021-09-15T00:48:38.933Z \#EXTINF:6.000, a/video\_segment\_1\_11352692.mp4 \#EXTINF:6.000, a/video\_segment\_1\_11352693.mp4 \#EXTINF:6.000, a/video\_segment\_1\_11352694.mp4 \#EXTINF:6.000, a/video\_segment\_1\_11352695.mp4 \#EXTINF:6.000, a/video\_segment\_1\_11352696.mp4 Media playlist (B Variant) \#EXTM3U \#EXT-X-VERSION:6 \#EXT-X-INDEPENDENT-SEGMENTS \#EXT-X-TARGETDURATION:6 \#EXT-X-MEDIA-SEQUENCE:11352692 \#EXT-X-MAP:URI="video\_init\_1.mp4" \#EXT-X-PROGRAM-DATE-TIME:2021-09-15T00:48:38.933Z \#EXTINF:6.000, b/video\_segment\_1\_11352692.mp4 \#EXTINF:6.000, b/video\_segment\_1\_11352693.mp4 \#EXTINF:6.000, b/video\_segment\_1\_11352694.mp4 \#EXTINF:6.000, b/video\_segment\_1\_11352695.mp4 \#EXTINF:6.000, b/video\_segment\_1\_11352696.mp4 When the ingested content is not watermarked anymore, then:

<a id="ssp-us-prior-art-c8-para-00149"></a>
For DASH content, the EssentialProperty
Period shall be created with a single AdaptationSet
any information on the Variant location (in the example above, the
value of the SegmentTemplate element).
ETSI TS 104 002 V1.1.1 (2023-08)
WATERMARKING-VARIANT="b"
WATERMARKING-VARIANT="b"
WATERMARKING-VARIANT="a"
WATERMARKING-VARIANT="b"
EXT-X-MEDIA tags with the same GROUP\_ID value,
value. As these playlists are not for devices to consume and to minimize the
EXT-X-MEDIA share
elements shall be removed from the ingest manifest and a new
. The path to the segments shall be updated, removing
a/ shall be removed from the @media
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00150"></a>

---

<a id="ssp-us-prior-art-c8-header-00151"></a>
### Page 23

- <a id="ssp-us-prior-art-c8-bulletlist-00152"></a> <a id="ssp-us-prior-art-c8-list-item-00153"></a> <a id="ssp-us-prior-art-c8-empty-list-item-00154"></a>

<a id="ssp-us-prior-art-c8-para-00155"></a>
For HLS content, the encoder shall create a new multivariant playlist that does not include
VARIANT
information on the Variant location (in the example above, the
NOTE 3: Stopping watermarking content is different from toggling edge sequencing logic (see clause 5.3).
5.6.4.3
Locating the Sidecar File
The sidecar file is part of the ingest with the DASH manifest or HLS playlist, the link to this file is added in different
places depending on the format.
DASH ingest manifests shall include an EssentialProperty
@schemeIdUri attribute equal to
attribute equal to the pointer to the sidecar file. The pointer is relative to the ingest manifest.
The following is an example of a DASH ingest manifest where the watermarking signalling is highlighted in bold. In
this example, the absolute path for the sidecar file for the first representation is equal to
[https://dash\.edgesuite\.net/dash264/TestCases/1a/ElephantsDream\_H264BPL30\_0100\.264\.dash\_wm\_pace\_info](https://dash.edgesuite.net/dash264/TestCases/1a/ElephantsDream_H264BPL30_0100.264.dash_wm_pace_info).
NOTE:
EssentialProperty elements are added in the

<a id="ssp-us-prior-art-c8-rawblock-00156"></a>
```
<?xml version="1.0" encoding="UTF-8"?>

```

<a id="ssp-us-prior-art-c8-para-00157"></a>
\<MPD xmlns:xsi="[http://www\.w3\.org/2001/XMLSchema-instance](http://www.w3.org/2001/XMLSchema-instance)"
xmlns="urn:mpeg💨schema:mpd:2011"
xsi:schemaLocation="urn:mpeg💨schema:mpd:2011 DASH-MPD.xsd"
type="static"
mediaPresentationDuration="PT654S"
minBufferTime="PT4S"
…
`<AdaptationSet mimeType="video/mp4" codecs="avc1.42401E" subsegmentAlignment="true"
subsegmentStartsWithSAP="1" contentType='video' maxWidth="480" maxHeight="360"
maxFrameRate="24" par="4:3">`
`<Representation id="2" bandwidth="150000" width="480" height="360" frameRate="24">`
`<EssentialProperty
schemeIdUri="http://dashif.org/guidelines/watermarking_variant#a" value="tv1"/>`
`<EssentialProperty
schemeIdUri="http://dashif.org/guidelines/watermarking_wmpaceinfo"
value="ElephantsDream_H264BPL30_0100.264.dash_wm_pace_info"/>`
`<BaseURL>`a/ElephantsDream\_H264BPL30\_0100.264.dash`</BaseURL>`
`<SegmentBase indexRange="984-11244">`
`<Initialization range="0-983"/>`
`</SegmentBase>`
`</Representation>`
`<Representation id="3" bandwidth="250000" width="480" height="360" frameRate="24">`
`<EssentialProperty
schemeIdUri="http://dashif.org/guidelines/watermarking_variant#a" value="tv1"/>`
`<EssentialProperty
schemeIdUri="https://dashif.org/guidelines/watermarking_wmpaceinfo"
value="ElephantsDream_H264BPL30_0175.264.dash_wm_pace_info"/>`
`<BaseURL>`a/ElephantsDream\_H264BPL30\_0175.264.dash`</BaseURL>`
`<SegmentBase indexRange="984-11245">`
`<Initialization range="0-983"/>`
`</SegmentBase>`
`</Representation>`
…
`</AdaptationSet>`
`</MPD>`
HLS ingest playlists shall include in the media playlist a custom tag specifying the pointer to the sidecar file. The
pointer is relative to the ingest manifest. The tag is
attribute is URI
(A, B, C …), the sidecar file referenced by the \#EXT-X-WMPACEINFO
considered.
ETSI TS 104 002 V1.1.1 (2023-08)
WATERMARKING-
attributes. It also stops delivering the additional media playlists for the B Variant and others if
present. The path to the segments in the media playlist delivered to devices shall be updated, removing any
a/ shall be removed from the media playlist).
element at the Representation level with a
[http://dashif\.org/guidelines/watermarking\_wmpaceinfo](http://dashif.org/guidelines/watermarking_wmpaceinfo) and @value
This example also includes the signalling defined in clause 5.6.2 (for one Variant A). In this case, the
Representation.
\#EXT-X-WMPACEINFO:`<attribute-list>` where the defined
, a quoted-string that gives the relative pointer to the sidecar file. In the media playlist for each Variant
tag is the same as the variant value shall not be
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00158"></a>

---

<a id="ssp-us-prior-art-c8-header-00159"></a>
### Page 24

<a id="ssp-us-prior-art-c8-header-00160"></a>
## The following is an example of a HLS media playlist, the watermarking signalling is highlighted in bold. Note that the multivariant playlist remains unmodified. \#EXTM3U \#EXT-X-TARGETDURATION:8 \#EXT-X-VERSION:7 \#EXT-X-MEDIA-SEQUENCE:1 \#EXT-X-PLAYLIST-TYPE:VOD \#EXT-X-INDEPENDENT-SEGMENTS \#EXT-X-WMPACEINFO:URI="main\_wm\_pace\_info" \#EXT-X-MAP:URI="main.mp4",BYTERANGE="1118@0" \#EXTINF:7.98333, \#EXT-X-BYTERANGE:1700094@1118 a/main.mp4 \#EXTINF:8.00000, \#EXT-X-BYTERANGE:1789481@1701212 a/main.mp4 \#EXTINF:8.00000, \#EXT-X-BYTERANGE:1777588@3490693 a/main.mp4 \#EXTINF:8.00000, \#EXT-X-BYTERANGE:1752144@5268281 a/main.mp4 \#EXTINF:7.26667, \#EXT-X-BYTERANGE:1563219@7020425 a/main.mp4 5.6.5 Packaging Recommendations This clause contains requirements where packaged content is served to devices. The goal is to facilitate the creation and management of A and B Variants in the delivery chain. These requirements apply even if no re-packaging process exists. NOTE: publishes egress versions of the content directly. The minimum segment duration should consider the embedding capabilities of the WM technology in order to ensure or B) allows to match a segment to a bit value in the WM pattern. As described in clause 5.6.3, a re-packaging process may aggregate received parts of content. It builds a segment beginning with the part of content with firstpart=true segment until the targeted length has been reached. It shall begin creating a new segment if a part of content with firstpart=true inconsistent metadata, more precisely, only ingest segments carrying the same together. The transformation of ingest manifest into egress manifests requires the following actions:

<a id="ssp-us-prior-art-c8-header-00161"></a>
## All watermarking\_wmpaceinfo and manifests and EXT-X-WMPACEINFO

<a id="ssp-us-prior-art-c8-header-00162"></a>
## $\{variantPath\}).

<a id="ssp-us-prior-art-c8-header-00163"></a>
## DASH manifests shall be made neutral (without While the manifests are made neutral when delivered to devices, the content shall remain stored with the structure defined in the ingest manifests. Doing so, when the CDN edge requests a Variant for a given segment in applying the logic defined in clause 5.7.5, the origin has a direct access to the requested Variant. Additionally, when translating from ingress to egress, a re-packaging process shall:

<a id="ssp-us-prior-art-c8-para-00164"></a>
overwrite WMPaceInfo
shall prevent start code emulation. It is recommended to overwrite with
ETSI TS 104 002 V1.1.1 (2023-08)
This implies that an encoder working against a completely passive receiver (e.g. interface 2 of \[i.1\])
that a segment contains only information for A or B Variant. A segment carrying only one bit of information (Variant A
and then aggregates until lastpart=true for creating a
is received before reaching the targeted length. The packager shall not aggregate segments that have
position value shall be aggregated
watermarking\_variantEssentialProperty elements in DASH
tags in HLS playlists shall be removed from the egress manifests.
HLS media playlists of a given rendition in HLS shall be merged into a single, neutral version of it (without
$\{variantPath\}).
when carried as SEI messages, TS adaptation fields or ISOBMFF boxes. Overwriting
0xFF;
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00165"></a>

---

<a id="ssp-us-prior-art-c8-header-00166"></a>
### Page 25

<a id="ssp-us-prior-art-c8-para-00167"></a>
25 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-codeblock-00168"></a>
```
-    remove firstpart, lastpart, segmentRegex from sidecar-discrete elements.
```

<a id="ssp-us-prior-art-c8-para-00169"></a>
5.7 Content Playback

<a id="ssp-us-prior-art-c8-para-00170"></a>
5.7.1 Introduction

<a id="ssp-us-prior-art-c8-para-00171"></a>
The flow for content playback is shown in the following clauses. The origin received content as explained in clause 5.5.
It has access to the A/B Variants and the WMPaceInfo data.

<a id="ssp-us-prior-art-c8-para-00172"></a>
This clause describes only the case where the WM token is used in direct mode and does not consider the value of
wmsegduration (hence using WMPaceInfo).

<a id="ssp-us-prior-art-c8-para-00173"></a>
This clause is also not considering the case of download of content for later offline playback. Usually, content available
for download is available in the form of byteranges and the device requests large byteranges that overlap those
announced in the MPD or HLS playlists. When content is watermarked, this is not possible as only announced
byteranges are addressable (see clause 5.7.5.4). The device shall therefore either use the announced byteranges only or a
proxy shall ensure that the edge receives requests that are for announced byteranges.

<a id="ssp-us-prior-art-c8-para-00174"></a>
Content playback is divided in three actions:

<a id="ssp-us-prior-art-c8-codeblock-00175"></a>
```
-    Acquiring the WM token, the DASH manifest, or the HLS playlists

-    Acquiring the initialization segment

-    Acquiring media segments
```

<a id="ssp-us-prior-art-c8-para-00176"></a>
While the first action is common to all type of content, the other ones have variations depending on the packaging and
delivery mode of the content. Variation is, for example on the difference between content delivered as byterange or
discrete segments. Another possible variation appears when HLS low latency is used for the chunks requested at the
edge of live.

<a id="ssp-us-prior-art-c8-para-00177"></a>
The following goes through the different actions by providing the expected workflows.

<a id="ssp-us-prior-art-c8-para-00178"></a>
5.7.2 Dynamic Ad Insertion

<a id="ssp-us-prior-art-c8-para-00179"></a>
In case of Dynamic Ad Insertion (DAI), the break may happen at any time. As every segment carries watermarking
information allowing to perform the detection, there shall not be segments carrying conflicting data. While some
techniques may recover from this mix of data, it will, in all cases, impact the length of content needed for retrieving the
unique identifier.

<a id="ssp-us-prior-art-c8-para-00180"></a>
For Live content, assuming that an ad replacement period is defined, then from the device perspective, the following
consumption modes are possible.

<a id="ssp-us-prior-art-c8-codeblock-00181"></a>
```
-    The device consumes ads from an alternative edge for the full duration of the ad break

-    The device consumes ads from an alternative edge for a duration shorter than the replacement period

-    The device consumes the original content as no replacement ad is proposed
```

<a id="ssp-us-prior-art-c8-para-00182"></a>
Devices may therefore consume content differently during the ad break.

<a id="ssp-us-prior-art-c8-para-00183"></a>
For VOD content, ads will be inserted or stitched with ad break (cue in/out points for example) markers. The device
should consume them from an alternative edge for the full duration of the ad break.

<a id="ssp-us-prior-art-c8-para-00184"></a>
The encoder shall watermark ads part of the original content for Live content. The watermarking technology shall
remain consistent between all these options. Some devices may receive the original content if no ad can be found for
replacement. One consequence is that these devices receive content that is meant to be watermarked following the rules
of the present document.

<a id="ssp-us-prior-art-c8-para-00185"></a>
Devices receiving an ad for replacement shall receive it from a different edge that does not enforce watermarking. Such
edge will then gracefully ignore the WM token.

<a id="ssp-us-prior-art-c8-codeblock-00186"></a>
```
                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00187"></a>

---

<a id="ssp-us-prior-art-c8-header-00188"></a>
### Page 26

<a id="ssp-us-prior-art-c8-para-00189"></a>
26 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00190"></a>
The WM token is expected to be present in all playback requests during the session. In presence of a DAI manifest
manipulator, depending on its behaviour, it may be necessary to tweak the configuration of the delivery pipeline to
guarantee the propagation of the WM token. For instance, it may be required to perform some manifest manipulation at
the edge to re-introduce the WM token in the response, e.g. when the token is transported as a query parameter and the
DAI manifest manipulator is not piggybacking incoming query parameters in the rewritten manifest/playlist. Another
case is when the watermark token is incorporated to the virtual path, stripped at the edge on its way to the DAI manifest
manipulator (that remains therefore unaware of the WM token) which returns a manipulated playlist that contains
absolute URLs.

<a id="ssp-us-prior-art-c8-para-00191"></a>
5.7.3 WM Token, DASH Manifest and HLS Playlists Acquisition

<a id="ssp-us-prior-art-c8-para-00192"></a>
The device acquires the WM token in an implementation specific manner. It may be retrieved directly from a WM
token server, or it may be provided in a response from another server as part of other data required for playing back
content.

<a id="ssp-us-prior-art-c8-para-00193"></a>
The WM token may be added as part of the virtual path of the requested object, as a query string attribute or as part of
the HTTP header when the device requests content to the edge. It is recommended to use the virtual path.

<a id="ssp-us-prior-art-c8-para-00194"></a>
The WM token may be added by the device for requesting DASH manifest and HLS playlists. While these objects are
not watermarked (the pattern in the name allows the edge to know this), the edge may validate or not the token and
refuse to serve these objects if the token is not valid. The edge may also gracefully ignore the token. The origin cleans
the served objects, removing any property related to location of objects (see clause 5.6.5). The manifest and playlist are
neutral. This is summarized in Figure 5.

<a id="ssp-us-prior-art-c8-codeblock-00195"></a>
```
               Figure 5: Token, DASH manifest and HLS playlist acquisition

                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00196"></a>

---

<a id="ssp-us-prior-art-c8-header-00197"></a>
### Page 27

<a id="ssp-us-prior-art-c8-para-00198"></a>
5.7.4
Initialization Segment Acquisition
When content is delivered as byteranges, as the initialization segment is within the file, the token shall be added in the
request as the requested file has a name that matches the pattern for watermarked content. The edge will then apply the
exact same logic it applies for a media segment, it retrieves the sidecar file and extracts the
part of the track that contains the initialization segment (as defined in clause 5.7.5). It can then deliver the initialization
segment to the device. As position
Variant A. One or several Variants may become unavailable on the origin for any reason, such as a lost connection with
available. The origin shall deliver to the edge the initialization segment from any available Variant in this case on the
endpoint for Variant A.
NOTE:
segment and a media segment.
When content is delivered as discrete segments, the name of the initialization segment shall not match the pattern for
watermarked content as written in clause 5.3. The WM token may be added by the device for requesting the
initialization segment. The edge may validate it or not and may refuse to serve these objects if it is not valid. The edge
may also gracefully ignore it.
5.7.5
Media Segments and WMPaceInfo Acquisition
5.7.5.1
General Requirements
For the media segments, a token shall be attached to the HTTP requests. If not present, the edge shall reject the request
and shall not deliver the segment. The edge shall validate the WM token (that can include checking signed data or
sequenced.
Watermarked objects shall include in the sub-path in the edge forward requests to the origin the value of identifying
Variants that is part of the configuration described in clause 5.3. A request received at the CDN edge for
[https://edge\.hostname/path/to/endpoint/video\_segment\_5\_8353305\.mp4](https://edge.hostname/path/to/endpoint/video_segment_5_8353305.mp4) shall be translated into a forward request for
[https://origin\.hostname/path/to/endpoint/$\{variantPath\}](https://origin.hostname/path/to/endpoint/%24%7BvariantPath%7D)
$\{variantPath\}
watermarking is done through audio segments.
The connection between the origin and the edge shall be restricted to legitimate requests. How this is achieved is out of
the scope of the present document.
tools for restricting the access.
There may be the need to disable watermarking within or upstream of the packager at any time, for example, one or
several Variants may become unavailable on the origin for any reason, such as a lost connection with the encoder for
these encoding pipelines. As devices request all Variants, this situation will result in intermittent black screens when
requesting the affected Variants. In such case, position
Variant A. If this endpoint is not working properly, the origin shall deliver any available Variant on this endpoint.
document. As an example, the origin can raise an alarm.
ETSI TS 104 002 V1.1.1 (2023-08)
WMPaceInfo for the first
is equal to -1 (not watermarked), it shall deliver the initialization segment from
the encoder for these encoding pipelines. Such situation will result in a failed playback if Variant A is the one that is not
The token is evaluated and validated as the edge cannot make a difference between the initialization
decrypting some claims) which is attached to the requests and extracts the WM pattern so that the correct Variant can be
video\_segment\_5\_8353305.mp4 where the value of
depends on the value extracted from the WM pattern for this segment. The same logic applies if the
NOTE 1: A static secret (a shared key), dynamic signatures or access lists (based on IP addresses) are examples of
shall be set to -1 in WMPaceInfo, effectively announcing to
the edge sequencing logic that segments are not watermarked. The edge shall then consume segment on the endpoint for
NOTE 2: This is breaking the watermarking detection. The period when such contingency measure is applied is not
to be used for detection. How the end-to-end system is synchronized is out of the scope of the present
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00199"></a>

---

<a id="ssp-us-prior-art-c8-header-00200"></a>
### Page 28

<a id="ssp-us-prior-art-c8-header-00201"></a>
## 5.7.5.2 WMPaceInfo Acquisition For each device request for /pathname/filename associated to this object. The origin presents this information differently whether segments are discrete or byteranges:

<a id="ssp-us-prior-art-c8-header-00202"></a>
## For byterange segment, the origin shall have a dedicated endpoint for delivering sidecar file. For a segment requested by a device at /pathname/WMPaceInfo/filename and only provide the sidecar file to the edge. The

<a id="ssp-us-prior-art-c8-header-00203"></a>
## For discrete segment, the origin:

<a id="ssp-us-prior-art-c8-header-00204"></a>
## Shall have a dedicated endpoint WMPaceInfo object. The Content-Type

<a id="ssp-us-prior-art-c8-header-00205"></a>
## Shall add WMPaceInfo WMPaceInfoEgress

<a id="ssp-us-prior-art-c8-header-00206"></a>
## It is the edge that defines which endpoint it uses. If WMPaceInfo was delivered to the origin in ingress form (as part of the HTTP request headers, SEI message, ISOBMFF box, TS adaptation field or a sidecar file per track), that data shall be extracted and made available in egress form to the edge as both a HTTP header and dedicated endpoint. Any direct request from a device with /pathname/WMPaceInfo/filename Table 5 gives examples of content flows as ingest to the origin and egress of the origin to the edge. Live content No sidecar file, data is delivered as part of Ingest of the origin HTTP headers, SEI messages, ISOBMFF boxes or TS adaptation field. One sidecar file per segment (note the special case of HLS low latency with byterange where Egress of the origin multiple chunks are be linked to the same sidecar file, see clause 5.7.5.4) and HTTP header. There are then three endpoints on the origin:

<a id="ssp-us-prior-art-c8-header-00207"></a>
## WMPaceInfo: /pathname/WMPaceInfo/filename

<a id="ssp-us-prior-art-c8-header-00208"></a>
## Variant A: /pathname/$\{variantPath\}filename

<a id="ssp-us-prior-art-c8-header-00209"></a>
## Variant B: /pathname/$\{variantPath\}filename Where $\{variantPath\} is as defined in clause 5.3. NOTE: Adding Variants creates additional endpoints. 5.7.5.3 Discrete Files For the media segments delivered as discrete files, the flow is shown in Figure 6. The edge sequences the A or B Variant of a segment based on the WM pattern contained in the token. It has two options to know the position of the segment within the WM pattern:

<a id="ssp-us-prior-art-c8-para-00210"></a>
First make a request to the origin to retrieve the
path /pathname/WMPaceInfo/filename.
payload of the response as a sidecar file.
ETSI TS 104 002 V1.1.1 (2023-08)
, the edge shall retrieve from the origin egress WMPaceInfo data
WMPaceInfo information as a
/pathname/filename, the origin shall have an endpoint
that makes the sidecar file available. The response payload shall
contain the sidecar file (as defined in clause 5.5.3.2 for byterange segments). The origin shall not extract data
Content-Type for this object is application/cbor.
/pathname/WMPaceInfo/filename for delivering WMPaceInfo for
the requested segment. The response payload shall contain a sidecar file that contain a single
for this object is application/cbor.
in the response header (as defined in clause 5.5.3.3) under the
header field when the edge requests the segment.
shall receive an error code 403.
Table 5: Examples of content flows
VOD content
For both discrete segments and byteranges,
one sidecar file per track.
For discrete segments, one sidecar file per
segment and HTTP header.
For byterange, one sidecar file per track.
WMPaceInfo data. This is done with a GET request using the
The origin provides the WMPaceInfo from the Variant A in the
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00211"></a>

---

<a id="ssp-us-prior-art-c8-header-00212"></a>
### Page 29

- <a id="ssp-us-prior-art-c8-bulletlist-00213"></a> <a id="ssp-us-prior-art-c8-list-item-00214"></a> <a id="ssp-us-prior-art-c8-empty-list-item-00215"></a>

<a id="ssp-us-prior-art-c8-header-00216"></a>
## Once, the data in WMPaceInfo origin the right Variant corresponding to the position in the WM pattern that matches the value of in WMPaceInfo and then deliver it to the device.

<a id="ssp-us-prior-art-c8-para-00217"></a>
Make a request for the A and B Variants, extract the
data in WMPaceInfo
to the device.
NOTE:
There is a high probability that the edge will request both A and B Variants, hence adding
to the response header allows avoiding an extra request to the origin.
The edge caches the Variants of a given segment with different cache keys and it should prevent the cache keys to be
revealed through debug headers.
ETSI TS 104 002 V1.1.1 (2023-08)
is interpreted in conjunction with the WM pattern, the edge can request to the
position
WMPaceInfo from one response header and once, the
is interpreted in conjunction with the WM pattern, the edge can deliver the right Variant
WMPaceInfo
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00218"></a>

---

<a id="ssp-us-prior-art-c8-header-00219"></a>
### Page 30

<a id="ssp-us-prior-art-c8-para-00220"></a>
30 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00221"></a>
Figure 6: Media segment, as discrete file, acquisition

<a id="ssp-us-prior-art-c8-codeblock-00222"></a>
```
                   ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00223"></a>

---

<a id="ssp-us-prior-art-c8-header-00224"></a>
### Page 31

<a id="ssp-us-prior-art-c8-para-00225"></a>
5.7.5.4
Byterange
For the media segments delivered as byteranges, the flow is shown in Figure 7. The edge delivers the A or B Variant of
a segment based on the WM pattern contained in the token. To know which position in the WM pattern it has to
consider, it needs to retrieve the sidecar file associated to this track. It first makes a HTTP GET request to the origin in
order to retrieve the sidecar file.
Whilst sub ranges within segments, such as chunks, are allowed, the edge shall not deliver byteranges overlapping
several segments with different position values in WMPaceInfo
NOTE 1: An example is content delivered with HLS using the
to the origin and will receive a sidecar file with only one
it does not have enforce byterange validation for these requests.
Once the data in WMPaceInfo
Variant corresponding to the position in the WM pattern that matches the value of
ETSI TS 104 002 V1.1.1 (2023-08)
.
EXT-X-PART tag are byterange requests within a
discrete segment. When the edge receives the request for this partial segment, it will request WMPaceInfo
WMPaceInfo. This allows the edge to know that
NOTE 2: Only byteranges overlapping valid ranges are problematic, requests for byteranges included in an allowed
range are not breaking the WM pattern that is created by the A/B Variants and thus can be served.
is interpreted in conjunction with the WM pattern, the edge can deliver the correct
position in WMPaceInfo.
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00226"></a>

---

<a id="ssp-us-prior-art-c8-header-00227"></a>
### Page 32

<a id="ssp-us-prior-art-c8-para-00228"></a>
32 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00229"></a>
Figure 7: Media segment, as byterange, acquisition

<a id="ssp-us-prior-art-c8-codeblock-00230"></a>
```
                  ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00231"></a>

---

<a id="ssp-us-prior-art-c8-header-00232"></a>
### Page 33

<a id="ssp-us-prior-art-c8-para-00233"></a>
33 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00234"></a>
5.8 Monitoring and Watermark Detection

<a id="ssp-us-prior-art-c8-para-00235"></a>
If content is found, a detection of a WM pattern can be performed. A video acquisition that includes valuable content
(no commercial breaks for example) is performed. As the unique ID is obtained by extracting information from
segments (0 or 1 in every segment), the acquired content shall be of several minutes (the longer the segments are, the
longer the acquired video is). The video is then processed by the watermarking provider in order to extract the unique
ID. This ID is then provided to the relevant entity that can match it to a device, user or streaming session and take the
desired actions.

<a id="ssp-us-prior-art-c8-para-00236"></a>
How the detection is performed, and the revocation of the WM token is performed are out of the scope of the present
document.

<a id="ssp-us-prior-art-c8-codeblock-00237"></a>
```
                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00238"></a>

---

<a id="ssp-us-prior-art-c8-header-00239"></a>
### Page 34

<a id="ssp-us-prior-art-c8-para-00240"></a>
34 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00241"></a>
Annex A (normative):
Vendor Specific Core API

<a id="ssp-us-prior-art-c8-para-00242"></a>
A.1 Introduction

<a id="ssp-us-prior-art-c8-para-00243"></a>
In case of a token in indirect mode, it is expected that a vendor specific core (identified by wmvnd) generates the WM
pattern (referred as wmpattern). This means that this requires some interaction between the edge and this vendor
specific core. To facilitate this integration, the following defines the API made available by the vendor specific core.

<a id="ssp-us-prior-art-c8-para-00244"></a>
A.2 Edge-Vendor Specific API

<a id="ssp-us-prior-art-c8-para-00245"></a>
It is assumed that:

<a id="ssp-us-prior-art-c8-codeblock-00246"></a>
```
-    The call to the API function is blocking and the edge waits for the vendor specific core to end its processing.

-    The verification of the token is done before the call to the function. Verification includes the validation of the
     signature.
```

<a id="ssp-us-prior-art-c8-para-00247"></a>
The inputs are the values of the claims of the token that are relevant for the generation of the WM pattern.

<a id="ssp-us-prior-art-c8-para-00248"></a>
const crypto = require('crypto');

<a id="ssp-us-prior-art-c8-para-00249"></a>
function generate\_wmpattern (token.wmpatlen, token.wmkeyver, token.wmid, token.wmopid)
\{
/\* vendor specific processing \*/
return wmpattern;
\}

<a id="ssp-us-prior-art-c8-codeblock-00250"></a>
```
                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00251"></a>

---

<a id="ssp-us-prior-art-c8-header-00252"></a>
### Page 35

<a id="ssp-us-prior-art-c8-header-00253"></a>
## Annex B (informative): Examples of Workflows B.1 Introduction This annex takes the DASH-IF ingest protocol \[i.1\] as a reference. There are two interfaces defined:

<a id="ssp-us-prior-art-c8-header-00254"></a>
## to an active receiving entity as a Just In Time Packager (JITP).

<a id="ssp-us-prior-art-c8-header-00255"></a>
## MPD or playlist. Therefore, the receiving entity is either active (interface 1) or passive (interface 2) and this leads to the following possibilities:

<a id="ssp-us-prior-art-c8-header-00256"></a>
## CMAF ingest, active receiving entity (JITP)

<a id="ssp-us-prior-art-c8-header-00257"></a>
## HLS/DASH ingest, active receiving entity (JITP)

<a id="ssp-us-prior-art-c8-para-00258"></a>
HLS/DASH ingest, passive receiving entity
Given all the options for carrying WMPaceInfo
and VOD content.
B.2
Live Content Flows
For an active receiving entity
in clause 5.6.4, the manifests are sent. The JITP may aggregate ingress segments according to (
and WMPaceInfoEgress
properties) is removed from egress playlists.
If using the WMPaceInfoIngest
Figure B.1.
Active
Ingest Source
Receiving
Entity
PUT/ingest-segment
WMPaceInfoIngest: `<json>`
Another possible option is using sidecar file, this leads to the flow shown in Figure B.2.
ETSI TS 104 002 V1.1.1 (2023-08)
Interface 1, where the combination of packager and origin is able to perform additional re-packaging hence the
structure of ingest and egress may differ. Each POST/PUT contains one CMAF segment. This is often referred
Interface 2, where the combination of packager and origin does not perform additional re-packaging, the
structure of ingest and egress may be the same. The receiving entity is "passive", the source produces all
objects in form that devices can consume. Each POST/PUT implicitly refers to one addressable object in an
(see clause 5.5.3), the following describes some example flows for Live
(JITP), the grouping is non-trivial (as defined in \[i.1\] clause 6.2), therefore, as described
firstpart, lastpart)
will reflect the aggregated result. In addition, evidence of WM process (such as the essential
header field on interface 1, the flow from the encoder to the edge is shown in
JITP translates
WMPaceInfoIngest to
WMPaceInfoEgress upon
Store ingest-segment &
request from edge
WMPaceInfoIngest
Edge
GET/egress-segment
WMPaceInfoEgress: `<cbor>`
Figure B.1: Flow when using WMPaceInfoIngest and WMPaceInfoEgress header fields
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00259"></a>

---

<a id="ssp-us-prior-art-c8-header-00260"></a>
### Page 36

<a id="ssp-us-prior-art-c8-para-00261"></a>
Active
Ingest Source
Receiving
Entity
PUT/ingest-segment
WMPaceInfoIngest: `<json>`
Another option is using SEI data. In this case, the receiving entity, either leaves
and then overwrites it when serving after translating to
saves the WMPaceInfo data somewhere else. The flow shown in Figure B.3.
Active
Ingest Source
Receiving
Entity
PUT/ingest-segment
SEI: WMPaceInfo()
With a passive receiving entity
WMPaceInfo
flow with sidecar files.
Encoder only sends
egress WMPaceInfo in
sidecar file when
pushing to origin
Ingest Source
PUT/egress-segment
PUT/WMPaceInfo/egress-segment
ETSI TS 104 002 V1.1.1 (2023-08)
JITP translates
WMPaceInfoIngest to
sidecar file upon
Store ingest-segment &
request from edge
WMPaceInfoIngest
Edge
GET/WMPaceInfo/egress-segment
GET/egress-segment
Figure B.2: Flow when using WMPaceInfoIngest header field and sidecar file
WMPaceInfo in segment when storing
WMPaceInfoEgress header or overwrites it before storing and
JITP translates SEI to
WMPaceInfoEgress upon
Store ingest-segment &
request from edge
SEI
Edge
GET/egress-segment
WMPaceInfoEgress: `<cbor>`
Figure B.3: Flow when using SEI data and WMPaceInfoEgress header field
, there is no media manipulation downstream of ingest source, therefore transferring
data within the media is not an option, as it is not possible to overwrite it. Figure B.4 shows a possible
Store egress-segment &
Sidecar file
Passive
Edge
Receiving
Entity
GET/WMPaceInfo/egress-segment
GET/egress-segment
Figure B.4: Flow when using sidecar files
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00262"></a>

---

<a id="ssp-us-prior-art-c8-header-00263"></a>
### Page 37

<a id="ssp-us-prior-art-c8-para-00264"></a>
B.3
VOD Content Flows
If VOD content is prepared using live profile, then the permutations presented in clause B.2 are applicable. In addition,
another option is that a single sidecar can describe all segments using regex for
to the flow shown in Figure B.5.
For each segment of each representation
PUT/segment
Receiving
Ingest Source
Entity
After
PUT/WMPaceInfo/sidecar
PUT/manifest
If VOD content is prepared using on-demand profile, then the sidecar file is the only mechanism available to deliver
WMPaceInfo data. This leads to the flow shown in Figure B.6.
For each representation
PUT/trackfile
PUT/WMPaceInfo/trackfile
Receiving
Ingest Source
Entity
After
PUT/manifest
ETSI TS 104 002 V1.1.1 (2023-08)
segmentRegex. This latter case leads
Store segments,
sidecars and manifest
Edge
GET/egress-segment
GET/WMPaceInfo/sidecar
Figure B.5: Flow when using sidecar files for VOD live profile
Edge validates that
byteranges do not
overlap several
Store trackfiles,
segments with different
sidecars and manifest
position values
Edge
GET/manifest
GET/WMPaceInfo/trackfile
GET/trackfile
Figure B.6: Flow when using sidecar files for VOD on-demand profile
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00265"></a>

---

<a id="ssp-us-prior-art-c8-header-00266"></a>
### Page 38

<a id="ssp-us-prior-art-c8-para-00267"></a>
38 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00268"></a>
Annex C (normative):
Registration Requests

<a id="ssp-us-prior-art-c8-para-00269"></a>
C.1 General

<a id="ssp-us-prior-art-c8-para-00270"></a>
This annex contains the registration requests for IANA (token claims) and MP4RA (4CC code).

<a id="ssp-us-prior-art-c8-para-00271"></a>
C.2 IANA Considerations

<a id="ssp-us-prior-art-c8-para-00272"></a>
The present document requests IANA to register the following claims in the following registry:
[https://www\.iana\.org/assignments/cwt/cwt\.xhtml\#claims-registry](https://www.iana.org/assignments/cwt/cwt.xhtml#claims-registry) \[12\].

<a id="ssp-us-prior-art-c8-para-00273"></a>
Version Claim

<a id="ssp-us-prior-art-c8-codeblock-00274"></a>
```
-    Claim Name: wmver

-    Claim Description: The version of the WM Token

-   JWT Claim Name: wmver

-    Claim Key: 300

-    Claim Value Type: unsigned integer

-    Change Controller: DASH-IF

-     Specification Document(s): Clause 5.4 of the present document
```

<a id="ssp-us-prior-art-c8-para-00275"></a>
Technology Vendor Claim

<a id="ssp-us-prior-art-c8-codeblock-00276"></a>
```
-    Claim Name: wmvnd

-    Claim Description: The WM technology vendor

-   JWT Claim Name: wmvnd

-    Claim Key: 301

-    Claim Value Type: unsigned integer

-    Change Controller: DASH-IF

-     Specification Document(s): Clause 5.4 of the present document
```

<a id="ssp-us-prior-art-c8-para-00277"></a>
Pattern Length Claim

<a id="ssp-us-prior-art-c8-codeblock-00278"></a>
```
-    Claim Name: wmpatlen

-    Claim Description: The length in bits of the WM pattern

-   JWT Claim Name: wmpatlen

-    Claim Key: 302

-    Claim Value Type: unsigned integer

-    Change Controller: DASH-IF

-     Specification Document(s): Clause 5.4 of the present document

                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00279"></a>

---

<a id="ssp-us-prior-art-c8-header-00280"></a>
### Page 39

<a id="ssp-us-prior-art-c8-para-00281"></a>
39 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00282"></a>
Segment Duration Claim

<a id="ssp-us-prior-art-c8-codeblock-00283"></a>
```
-    Claim Name: wmsegduration

-    Claim Description: The nominal duration of a segment

-   JWT Claim Name: wmsegduration

-    Claim Key: 303

-    Claim Value Type: map

-    Change Controller: DASH-IF

-     Specification Document(s): Clause 5.4 of the present document
```

<a id="ssp-us-prior-art-c8-para-00284"></a>
Pattern Claim

<a id="ssp-us-prior-art-c8-codeblock-00285"></a>
```
-    Claim Name: wmpattern

-    Claim Description: The WM pattern

-   JWT Claim Name: wmpattern

-    Claim Key: 304

-    Claim Value Types: COSE_Encrypt0 or COSE_Encrypt or byte string

-    Change Controller: DASH-IF

-     Specification Document(s): Clause 5.4 of the present document
```

<a id="ssp-us-prior-art-c8-para-00286"></a>
ID Claim

<a id="ssp-us-prior-art-c8-codeblock-00287"></a>
```
-    Claim Name: wmid

-    Claim Description: Used as input to derive the WM pattern for indirect mode

-   JWT Claim Name: wmid

-    Claim Key: 305

-    Claim Value Type: text string

-    Change Controller: DASH-IF

-     Specification Document(s): Clause 5.4 of the present document
```

<a id="ssp-us-prior-art-c8-para-00288"></a>
Operator ID Claim

<a id="ssp-us-prior-art-c8-codeblock-00289"></a>
```
-    Claim Name: wmopid

-    Claim Description: Used as additional input to derive the WM pattern for indirect mode

-   JWT Claim Name: wmopid

-    Claim Key: 306

-    Claim Value Type: unsigned integer

-    Change Controller: DASH-IF

-     Specification Document(s): Clause 5.4 of the present document
```

<a id="ssp-us-prior-art-c8-para-00290"></a>
Key Version Claim

<a id="ssp-us-prior-art-c8-codeblock-00291"></a>
```
-    Claim Name: wmkeyver

-    Claim Description: The key to use for derivation of the WM pattern in indirect mode

                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00292"></a>

---

<a id="ssp-us-prior-art-c8-header-00293"></a>
### Page 40

- <a id="ssp-us-prior-art-c8-bulletlist-00294"></a> <a id="ssp-us-prior-art-c8-list-item-00295"></a> <a id="ssp-us-prior-art-c8-empty-list-item-00296"></a>

<a id="ssp-us-prior-art-c8-header-00297"></a>
## JWT Claim Name: wmkeyver

<a id="ssp-us-prior-art-c8-header-00298"></a>
## Claim Key: 307

<a id="ssp-us-prior-art-c8-header-00299"></a>
## Claim Value Type: unsigned integer

<a id="ssp-us-prior-art-c8-header-00300"></a>
## Change Controller: DASH-IF

<a id="ssp-us-prior-art-c8-para-00301"></a>
Specification Document(s): Clause 5.4 of the present document
C.3
MP4RA Registration
The present document requests MP4RA to register the following 4CC code.
1)
The name, address, and URL of the organization requesting the code-point.
DASH-IF
3855 SW 153rd Dr., Beaverton, OR 97003, USA
[https://dashif\.org/](https://dashif.org/)
2)
The kind of code-point you wish to register (please choose from the set of registered types).
Boxes (Atoms)
3)
thought of as plain ASCII), but at most from the first 256 Unicode characters.
wmpi
4)
The specification in which this code-point is defined, if possible. A copy of the specification would be
in these files, would also be appreciated.
Available from here (
0.9.pdf).
5)
A brief 'abstract' of the meaning of the code-point, perhaps ten to twenty words.
wmpi
file.
6)
Contact information for an authorized representative for the code-point, including:
a)
Contact person's name, title, and organization:
DASH-IF Interoperability WG Chair
b)
Contact email:
[admin\@dashif\.org](mailto:admin@dashif.org)
7)
Date of definition or implementation (if known) or intended date (if in future).
July 31, 2023.
8)
Statement of an intention to apply (implement) the assigned code-point.
in the specification.
ETSI TS 104 002 V1.1.1 (2023-08)
For all except object-type registrations, the suggested identifier (four-character code). Note that fourcharacter codes use four 8-bit printable characters, usually from the first 128 Unicode characters (commonly
appreciated, as it enables the authority to understand the registration better. If you are requesting a 'codec'
code-point, a reference to the definition of the coding system itself, if separate from the definition of its storage
[https://dashif\.org/docs/IOP-Guidelines/DASH-IF-CTS-00XX-AB-Watermarkingstands](https://dashif.org/docs/IOP-Guidelines/DASH-IF-CTS-00XX-AB-Watermarkingstands) for WaterMarkPaceInfo. It carries A/B forensic watermarking information within the ISOBMFF
Expected to be implemented as part of DASH-IF conformance and reference tools according to the boilerplate
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00302"></a>

---

<a id="ssp-us-prior-art-c8-header-00303"></a>
### Page 41

<a id="ssp-us-prior-art-c8-para-00304"></a>
41 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00305"></a>
Annex D (informative):
Code for Web Sequence Diagram

<a id="ssp-us-prior-art-c8-para-00306"></a>
D.1 Introduction

<a id="ssp-us-prior-art-c8-para-00307"></a>
This annex provides is the code for generating all workflows shown in Figures 3 to 7, excluding Figure 4 to be used on
[https://websequencediagrams\.com](https://websequencediagrams.com) \[i.2\].

<a id="ssp-us-prior-art-c8-para-00308"></a>
D.2 Figure 3

<a id="ssp-us-prior-art-c8-para-00309"></a>
Participant Encoder
Participant Packager
Participant Origin

<a id="ssp-us-prior-art-c8-header-00310"></a>
# STEP 1: Ingest from the encoder to the packager

<a id="ssp-us-prior-art-c8-header-00311"></a>
# For instance, the segmentation is 1s long

<a id="ssp-us-prior-art-c8-para-00312"></a>
Encoder -\> Packager: Ingest manifest
Encoder -\> Packager: Ingest segments Variant A\\n (w/ WMPaceInfo)
Encoder -\> Packager: Ingest segments Variant B\\n (w/ WMPaceInfo)

<a id="ssp-us-prior-art-c8-header-00313"></a>
# STEP 2: Ingest from the Packager to the Origin (e.g. 2S long segments)

<a id="ssp-us-prior-art-c8-header-00314"></a>
# The Packager has to aggregate several DASH segments to produce the distributed segment

<a id="ssp-us-prior-art-c8-para-00315"></a>
Packager-\> Origin: Egress manifest
Packager-\> Origin: Egress segments Variant A\\n (w/ WMPaceInfo)
Packager-\> Origin: Egress segments Variant B\\n (w/ WMPaceInfo)

<a id="ssp-us-prior-art-c8-para-00316"></a>
D.3 Figure 5

<a id="ssp-us-prior-art-c8-para-00317"></a>
Participant Origin
Participant CDN Edge
Participant Device

<a id="ssp-us-prior-art-c8-header-00318"></a>
# STEP 1: Acquire a WM token

<a id="ssp-us-prior-art-c8-para-00319"></a>
opt WM token acquisition
note over Origin,Device: Implementation specific
end

<a id="ssp-us-prior-art-c8-header-00320"></a>
# STEP 2: Get the DASH manifest or HLS playlist for the viewing session

<a id="ssp-us-prior-art-c8-para-00321"></a>
alt Obtain DASH manifest
Device-\>+CDN Edge: Get MPD(WM token)
opt Manifest cache miss
CDN Edge-\>+Origin: Get MPD
Origin-\>Origin: Create a neutral MPD
Origin--\>-CDN Edge: MPD
CDN Edge-\>CDN Edge: Cache MPD
end
CDN Edge--\>-Device: MPD
else Obtain HLS playlists
Device-\>+CDN Edge: Get multivariant/media playlist(WM token)
opt Multivariant/media playlist cache miss
CDN Edge-\>+Origin: Get multivariant/media playlist
Origin-\>Origin: Create neutral multivariant/media playlist
Origin--\>-CDN Edge: multivariant/media playlist
CDN Edge-\>CDN Edge: Cache multivariant/media playlist
end
CDN Edge--\>-Device: Multivariant/media playlist
end

<a id="ssp-us-prior-art-c8-codeblock-00322"></a>
```
                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00323"></a>

---

<a id="ssp-us-prior-art-c8-header-00324"></a>
### Page 42

<a id="ssp-us-prior-art-c8-para-00325"></a>
42 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00326"></a>
D.4 Figure 6

<a id="ssp-us-prior-art-c8-para-00327"></a>
Participant Origin
Participant CDN Edge
Participant Device

<a id="ssp-us-prior-art-c8-para-00328"></a>
loop Segment request for playback
Device-\>+CDN Edge: GET /pathname/segment\_i(WM token)
CDN Edge-\>CDN Edge: Validate WM token
alt Invalid WM token
CDN Edge--\>Device: 401 Unauthorized
else Valid WM token
alt Use the dedicated endpoint for WMPaceInfo
opt WMPaceInfo cache miss
CDN Edge-\>+Origin: GET /pathname/WMPaceInfo/segment\_i
note right of Origin
Origin retrieves WMPaceInfo for this segment and delivers it
end note
Origin--\>-CDN Edge: 200 OK response
CDN Edge -\>\> CDN Edge: Cache response
end
else Retreive WMPaceInfo from response header
opt Variants cache miss
CDN Edge-\>+Origin: GET /pathname/${variantPath}segment_i
Origin-->-CDN Edge: 200 OK response
CDN Edge ->> CDN Edge: Cache response
CDN Edge->+Origin: GET /pathname/$\{variantPath\}segment\_i
Origin--\>-CDN Edge: 200 OK response
CDN Edge -\>\> CDN Edge: Cache response
end
end
alt Invalid Request: no WMPaceInfo for this segment
CDN Edge--\>Device: 400 Bad Request
else Valid Request: WMPaceInfo available for this segment
CDN Edge -\>\> CDN Edge: Create WMPaceInfoObject from cache
CDN Edge -\>\> CDN Edge: VAR=getVariant(WM token, WMPaceInfoObject)
alt If using the dedicated endpoint for WMPaceInfo
opt Segment Variant cache miss
CDN Edge-\>+Origin: GET /pathname/${VAR}/segment_i
Origin-->-CDN Edge: 200 OK /pathname/$\{VAR\}/segment\_i
CDN Edge -\>\> CDN Edge: Cache /pathname/$\{VAR\}/segment\_i
end
end
CDN Edge--\>Device: 200 OK with /pathname/segment\_i(Variant $\{VAR\})
end
end
Device-\>Device: Play Content
End

<a id="ssp-us-prior-art-c8-para-00329"></a>
D.5 Figure 7

<a id="ssp-us-prior-art-c8-para-00330"></a>
Participant Origin
Participant CDN Edge
Participant Device

<a id="ssp-us-prior-art-c8-para-00331"></a>
loop Segment request for playback (including init segment)
Device-\>+CDN Edge: GET /pathname/filename(WM token, byterange)
CDN Edge-\>\>CDN Edge: Validate WM token
alt Invalid WM token
CDN Edge--\>Device: 401 Unauthorized
else Valid WM token
opt WMPaceInfo cache miss
CDN Edge-\>+Origin: GET /pathname/WMPaceInfo/filename
note right of Origin
Origin retrieves WMPaceInfo sidecar file for
this file and delivers it

<a id="ssp-us-prior-art-c8-codeblock-00332"></a>
```
                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00333"></a>

---

<a id="ssp-us-prior-art-c8-header-00334"></a>
### Page 43

<a id="ssp-us-prior-art-c8-para-00335"></a>
43 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-codeblock-00336"></a>
```
        end note
        Origin-->-CDN Edge: 200 OK response
        CDN Edge ->> CDN Edge: Cache response
    end
    alt Invalid Request: no WMPaceInfo for this file
        CDN Edge-->Device: 400 Bad Request
    else Valid Request: WMPaceInfo available for this file (one or many objects)
        CDN Edge ->> CDN Edge: Create WMPaceInfoObjects list from cache payload
        CDN Edge ->> CDN Edge: WMPaceInfoObject=getObject(WMPaceInfoObjects,
```

<a id="ssp-us-prior-art-c8-para-00337"></a>
byterange)
alt Invalid byterange request
CDN Edge--\>Device: 400 Bad Request (Invalid byterange)
else Valid byterange request
CDN Edge -\>\> CDN Edge: VAR=getVariant(WM token, WMPaceInfoObject)
opt Byterange cache miss
CDN Edge-\>+Origin: Get /pathname/${VAR}/filename(byterange)
note right of Origin
The returned payload may be larger than the requested
byterange (Partial Object Caching)
end note
Origin-->-CDN Edge: 206 Partial Content
CDN Edge ->> CDN Edge: Cache /pathname/$\{VAR\}/filename(byterange)
end
opt Partial Object Caching
CDN Edge-\>\>CDN Edge: Construct byterange response from locally cached
object\\n/pathname/$\{VAR\}/filename(byterange)
end
CDN Edge--\>Device: 206 Partial Content
end
end
end
Device-\>Device: Play Content
End

<a id="ssp-us-prior-art-c8-codeblock-00338"></a>
```
                                          ETSI
```

<a id="ssp-us-prior-art-c8-horizontalrule-00339"></a>

---

<a id="ssp-us-prior-art-c8-header-00340"></a>
### Page 44

<a id="ssp-us-prior-art-c8-para-00341"></a>
Annex E (informative):
Change History
Date
Version
2022-03-23
0.8.0
Version published for first community review.
2023-02-02
0.9.0
Version published for second community review.
2023-02-09
0.9.1
Added IANA and MP4RA registration annexes.
(Editorial) Changed Master to Multivariant (HLS).
Removed remaining "must" from the text.
Added COSE\_Encrypt
2023-05-02
0.9.2
Updates on the variantPath
Deleted examples for token claims.
Clarified the storage paths for the Variant on the origin.
Clarified the order of the bits in the WM pattern.
2023-05-03
0.9.3
2023-05-09
0.9.5
Version created for IPR Review and ETSI Submission.
ETSI TS 104 002 V1.1.1 (2023-08)
Information about changes
(Editorial) Corrections on broken automatic references and few formatting issues.
(IANA) Updated the sidecar file integer keys and claim keys with final values.
option for wmpattern.
construction options (removed the '.' possibility).
Changed the encryption algorithm for the pattern (align with CTA WAVE CAT).
Version published for IOP Review with some small editorial updates.
ETSI

<a id="ssp-us-prior-art-c8-horizontalrule-00342"></a>

---

<a id="ssp-us-prior-art-c8-header-00343"></a>
### Page 45

<a id="ssp-us-prior-art-c8-para-00344"></a>
45 ETSI TS 104 002 V1.1.1 (2023-08)

<a id="ssp-us-prior-art-c8-para-00345"></a>
History

<a id="ssp-us-prior-art-c8-codeblock-00346"></a>
```
                          Document history
```

<a id="ssp-us-prior-art-c8-para-00347"></a>
V1.1.1 August 2023 Publication

<a id="ssp-us-prior-art-c8-codeblock-00348"></a>
```
                                          ETSI
```

<a id="ssp-review-metadata"></a>
## Structured-source metadata

| Field | Current value |
|---|---|
| Document ID | us-prior-art-c8 |
| Artifact family | prior-art-transcription |
| Jurisdiction | US |
| Scope | prior-art |
| Status | review-aid |
| Language | en |
| Title | C8 — ETSI TS 104 002 V1.1.1 (2023-08) — DASH-IF Forensic A/B Watermarking |
| Authority scheme | PDF evidence transcription |

<a id="ssp-review-dependencies"></a>
## Dependencies

| Kind | Subject | Exact semantic digest |
|---|---|---|
| None | — | — |

<a id="ssp-review-provenance"></a>
## Provenance

| Fragment | Stored source | Page | Region | Uncertainty |
|---|---|---:|---|---|
| [us-prior-art-c8-blockquote-00002](#ssp-us-prior-art-c8-blockquote-00002) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c8-bulletlist-00070](#ssp-us-prior-art-c8-bulletlist-00070) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-bulletlist-00079](#ssp-us-prior-art-c8-bulletlist-00079) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-bulletlist-00107](#ssp-us-prior-art-c8-bulletlist-00107) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-bulletlist-00112](#ssp-us-prior-art-c8-bulletlist-00112) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-bulletlist-00118](#ssp-us-prior-art-c8-bulletlist-00118) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-bulletlist-00152](#ssp-us-prior-art-c8-bulletlist-00152) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c8-bulletlist-00213](#ssp-us-prior-art-c8-bulletlist-00213) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 29 | structured-transcription fragment | None declared |
| [us-prior-art-c8-bulletlist-00294](#ssp-us-prior-art-c8-bulletlist-00294) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00010](#ssp-us-prior-art-c8-codeblock-00010) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00016](#ssp-us-prior-art-c8-codeblock-00016) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00019](#ssp-us-prior-art-c8-codeblock-00019) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00022](#ssp-us-prior-art-c8-codeblock-00022) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00024](#ssp-us-prior-art-c8-codeblock-00024) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00043](#ssp-us-prior-art-c8-codeblock-00043) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00057](#ssp-us-prior-art-c8-codeblock-00057) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00168](#ssp-us-prior-art-c8-codeblock-00168) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00175](#ssp-us-prior-art-c8-codeblock-00175) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00181](#ssp-us-prior-art-c8-codeblock-00181) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00186](#ssp-us-prior-art-c8-codeblock-00186) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00195](#ssp-us-prior-art-c8-codeblock-00195) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00222](#ssp-us-prior-art-c8-codeblock-00222) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 30 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00230](#ssp-us-prior-art-c8-codeblock-00230) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 32 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00237](#ssp-us-prior-art-c8-codeblock-00237) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 33 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00246](#ssp-us-prior-art-c8-codeblock-00246) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00250](#ssp-us-prior-art-c8-codeblock-00250) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00274](#ssp-us-prior-art-c8-codeblock-00274) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00276](#ssp-us-prior-art-c8-codeblock-00276) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00278](#ssp-us-prior-art-c8-codeblock-00278) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00283](#ssp-us-prior-art-c8-codeblock-00283) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00285](#ssp-us-prior-art-c8-codeblock-00285) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00287](#ssp-us-prior-art-c8-codeblock-00287) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00289](#ssp-us-prior-art-c8-codeblock-00289) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00291](#ssp-us-prior-art-c8-codeblock-00291) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00322](#ssp-us-prior-art-c8-codeblock-00322) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00332](#ssp-us-prior-art-c8-codeblock-00332) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00336](#ssp-us-prior-art-c8-codeblock-00336) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 43 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00338](#ssp-us-prior-art-c8-codeblock-00338) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 43 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00346](#ssp-us-prior-art-c8-codeblock-00346) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 45 | structured-transcription fragment | None declared |
| [us-prior-art-c8-codeblock-00348](#ssp-us-prior-art-c8-codeblock-00348) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 45 | structured-transcription fragment | None declared |
| [us-prior-art-c8-empty-list-item-00072](#ssp-us-prior-art-c8-empty-list-item-00072) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-empty-list-item-00116](#ssp-us-prior-art-c8-empty-list-item-00116) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-empty-list-item-00154](#ssp-us-prior-art-c8-empty-list-item-00154) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c8-empty-list-item-00215](#ssp-us-prior-art-c8-empty-list-item-00215) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 29 | structured-transcription fragment | None declared |
| [us-prior-art-c8-empty-list-item-00296](#ssp-us-prior-art-c8-empty-list-item-00296) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00001](#ssp-us-prior-art-c8-header-00001) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c8-header-00007](#ssp-us-prior-art-c8-header-00007) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00014](#ssp-us-prior-art-c8-header-00014) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00026](#ssp-us-prior-art-c8-header-00026) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 3 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00029](#ssp-us-prior-art-c8-header-00029) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 4 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00032](#ssp-us-prior-art-c8-header-00032) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 5 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00035](#ssp-us-prior-art-c8-header-00035) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00045](#ssp-us-prior-art-c8-header-00045) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 7 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00048](#ssp-us-prior-art-c8-header-00048) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 8 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00051](#ssp-us-prior-art-c8-header-00051) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00059](#ssp-us-prior-art-c8-header-00059) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00062](#ssp-us-prior-art-c8-header-00062) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00063](#ssp-us-prior-art-c8-header-00063) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00064](#ssp-us-prior-art-c8-header-00064) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00065](#ssp-us-prior-art-c8-header-00065) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00068](#ssp-us-prior-art-c8-header-00068) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00069](#ssp-us-prior-art-c8-header-00069) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00073](#ssp-us-prior-art-c8-header-00073) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00074](#ssp-us-prior-art-c8-header-00074) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00075](#ssp-us-prior-art-c8-header-00075) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00076](#ssp-us-prior-art-c8-header-00076) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00077](#ssp-us-prior-art-c8-header-00077) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00083](#ssp-us-prior-art-c8-header-00083) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00086](#ssp-us-prior-art-c8-header-00086) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00087](#ssp-us-prior-art-c8-header-00087) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00088](#ssp-us-prior-art-c8-header-00088) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00089](#ssp-us-prior-art-c8-header-00089) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00090](#ssp-us-prior-art-c8-header-00090) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00093](#ssp-us-prior-art-c8-header-00093) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00094](#ssp-us-prior-art-c8-header-00094) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00095](#ssp-us-prior-art-c8-header-00095) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00096](#ssp-us-prior-art-c8-header-00096) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00097](#ssp-us-prior-art-c8-header-00097) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00100](#ssp-us-prior-art-c8-header-00100) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00101](#ssp-us-prior-art-c8-header-00101) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00102](#ssp-us-prior-art-c8-header-00102) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00103](#ssp-us-prior-art-c8-header-00103) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00104](#ssp-us-prior-art-c8-header-00104) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00105](#ssp-us-prior-art-c8-header-00105) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00111](#ssp-us-prior-art-c8-header-00111) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00126](#ssp-us-prior-art-c8-header-00126) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00127](#ssp-us-prior-art-c8-header-00127) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00128](#ssp-us-prior-art-c8-header-00128) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00129](#ssp-us-prior-art-c8-header-00129) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00130](#ssp-us-prior-art-c8-header-00130) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00131](#ssp-us-prior-art-c8-header-00131) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00134](#ssp-us-prior-art-c8-header-00134) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 19 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00137](#ssp-us-prior-art-c8-header-00137) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00138](#ssp-us-prior-art-c8-header-00138) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00139](#ssp-us-prior-art-c8-header-00139) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00140](#ssp-us-prior-art-c8-header-00140) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00141](#ssp-us-prior-art-c8-header-00141) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00144](#ssp-us-prior-art-c8-header-00144) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 21 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00147](#ssp-us-prior-art-c8-header-00147) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00148](#ssp-us-prior-art-c8-header-00148) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00151](#ssp-us-prior-art-c8-header-00151) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00159](#ssp-us-prior-art-c8-header-00159) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00160](#ssp-us-prior-art-c8-header-00160) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00161](#ssp-us-prior-art-c8-header-00161) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00162](#ssp-us-prior-art-c8-header-00162) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00163](#ssp-us-prior-art-c8-header-00163) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00166](#ssp-us-prior-art-c8-header-00166) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00188](#ssp-us-prior-art-c8-header-00188) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00197](#ssp-us-prior-art-c8-header-00197) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 27 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00200](#ssp-us-prior-art-c8-header-00200) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00201](#ssp-us-prior-art-c8-header-00201) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00202](#ssp-us-prior-art-c8-header-00202) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00203](#ssp-us-prior-art-c8-header-00203) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00204](#ssp-us-prior-art-c8-header-00204) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00205](#ssp-us-prior-art-c8-header-00205) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00206](#ssp-us-prior-art-c8-header-00206) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00207](#ssp-us-prior-art-c8-header-00207) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00208](#ssp-us-prior-art-c8-header-00208) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00209](#ssp-us-prior-art-c8-header-00209) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00212](#ssp-us-prior-art-c8-header-00212) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 29 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00216](#ssp-us-prior-art-c8-header-00216) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 29 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00219](#ssp-us-prior-art-c8-header-00219) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 30 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00224](#ssp-us-prior-art-c8-header-00224) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 31 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00227](#ssp-us-prior-art-c8-header-00227) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 32 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00232](#ssp-us-prior-art-c8-header-00232) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 33 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00239](#ssp-us-prior-art-c8-header-00239) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00252](#ssp-us-prior-art-c8-header-00252) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 35 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00253](#ssp-us-prior-art-c8-header-00253) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 35 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00254](#ssp-us-prior-art-c8-header-00254) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 35 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00255](#ssp-us-prior-art-c8-header-00255) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 35 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00256](#ssp-us-prior-art-c8-header-00256) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 35 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00257](#ssp-us-prior-art-c8-header-00257) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 35 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00260](#ssp-us-prior-art-c8-header-00260) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 36 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00263](#ssp-us-prior-art-c8-header-00263) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 37 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00266](#ssp-us-prior-art-c8-header-00266) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00280](#ssp-us-prior-art-c8-header-00280) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00293](#ssp-us-prior-art-c8-header-00293) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00297](#ssp-us-prior-art-c8-header-00297) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00298](#ssp-us-prior-art-c8-header-00298) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00299](#ssp-us-prior-art-c8-header-00299) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00300](#ssp-us-prior-art-c8-header-00300) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00303](#ssp-us-prior-art-c8-header-00303) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00310](#ssp-us-prior-art-c8-header-00310) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00311](#ssp-us-prior-art-c8-header-00311) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00313](#ssp-us-prior-art-c8-header-00313) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00314](#ssp-us-prior-art-c8-header-00314) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00318](#ssp-us-prior-art-c8-header-00318) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00320](#ssp-us-prior-art-c8-header-00320) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00324](#ssp-us-prior-art-c8-header-00324) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00334](#ssp-us-prior-art-c8-header-00334) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 43 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00340](#ssp-us-prior-art-c8-header-00340) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 44 | structured-transcription fragment | None declared |
| [us-prior-art-c8-header-00343](#ssp-us-prior-art-c8-header-00343) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 45 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00006](#ssp-us-prior-art-c8-horizontalrule-00006) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c8-horizontalrule-00013](#ssp-us-prior-art-c8-horizontalrule-00013) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00025](#ssp-us-prior-art-c8-horizontalrule-00025) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00028](#ssp-us-prior-art-c8-horizontalrule-00028) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 3 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00031](#ssp-us-prior-art-c8-horizontalrule-00031) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 4 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00034](#ssp-us-prior-art-c8-horizontalrule-00034) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 5 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00044](#ssp-us-prior-art-c8-horizontalrule-00044) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00047](#ssp-us-prior-art-c8-horizontalrule-00047) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 7 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00050](#ssp-us-prior-art-c8-horizontalrule-00050) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 8 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00058](#ssp-us-prior-art-c8-horizontalrule-00058) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00061](#ssp-us-prior-art-c8-horizontalrule-00061) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00067](#ssp-us-prior-art-c8-horizontalrule-00067) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00082](#ssp-us-prior-art-c8-horizontalrule-00082) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00085](#ssp-us-prior-art-c8-horizontalrule-00085) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00092](#ssp-us-prior-art-c8-horizontalrule-00092) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00099](#ssp-us-prior-art-c8-horizontalrule-00099) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00110](#ssp-us-prior-art-c8-horizontalrule-00110) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00125](#ssp-us-prior-art-c8-horizontalrule-00125) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00133](#ssp-us-prior-art-c8-horizontalrule-00133) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00136](#ssp-us-prior-art-c8-horizontalrule-00136) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 19 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00143](#ssp-us-prior-art-c8-horizontalrule-00143) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00146](#ssp-us-prior-art-c8-horizontalrule-00146) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 21 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00150](#ssp-us-prior-art-c8-horizontalrule-00150) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00158](#ssp-us-prior-art-c8-horizontalrule-00158) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00165](#ssp-us-prior-art-c8-horizontalrule-00165) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00187](#ssp-us-prior-art-c8-horizontalrule-00187) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00196](#ssp-us-prior-art-c8-horizontalrule-00196) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00199](#ssp-us-prior-art-c8-horizontalrule-00199) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 27 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00211](#ssp-us-prior-art-c8-horizontalrule-00211) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00218](#ssp-us-prior-art-c8-horizontalrule-00218) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 29 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00223](#ssp-us-prior-art-c8-horizontalrule-00223) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 30 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00226](#ssp-us-prior-art-c8-horizontalrule-00226) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 31 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00231](#ssp-us-prior-art-c8-horizontalrule-00231) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 32 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00238](#ssp-us-prior-art-c8-horizontalrule-00238) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 33 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00251](#ssp-us-prior-art-c8-horizontalrule-00251) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00259](#ssp-us-prior-art-c8-horizontalrule-00259) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 35 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00262](#ssp-us-prior-art-c8-horizontalrule-00262) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 36 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00265](#ssp-us-prior-art-c8-horizontalrule-00265) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 37 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00279](#ssp-us-prior-art-c8-horizontalrule-00279) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00292](#ssp-us-prior-art-c8-horizontalrule-00292) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00302](#ssp-us-prior-art-c8-horizontalrule-00302) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00323](#ssp-us-prior-art-c8-horizontalrule-00323) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00333](#ssp-us-prior-art-c8-horizontalrule-00333) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00339](#ssp-us-prior-art-c8-horizontalrule-00339) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 43 | structured-transcription fragment | None declared |
| [us-prior-art-c8-horizontalrule-00342](#ssp-us-prior-art-c8-horizontalrule-00342) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 44 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00071](#ssp-us-prior-art-c8-list-item-00071) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00080](#ssp-us-prior-art-c8-list-item-00080) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00108](#ssp-us-prior-art-c8-list-item-00108) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00113](#ssp-us-prior-art-c8-list-item-00113) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00115](#ssp-us-prior-art-c8-list-item-00115) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00119](#ssp-us-prior-art-c8-list-item-00119) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00121](#ssp-us-prior-art-c8-list-item-00121) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00123](#ssp-us-prior-art-c8-list-item-00123) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00153](#ssp-us-prior-art-c8-list-item-00153) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00214](#ssp-us-prior-art-c8-list-item-00214) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 29 | structured-transcription fragment | None declared |
| [us-prior-art-c8-list-item-00295](#ssp-us-prior-art-c8-list-item-00295) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00003](#ssp-us-prior-art-c8-para-00003) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c8-para-00004](#ssp-us-prior-art-c8-para-00004) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c8-para-00005](#ssp-us-prior-art-c8-para-00005) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c8-para-00008](#ssp-us-prior-art-c8-para-00008) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00009](#ssp-us-prior-art-c8-para-00009) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00011](#ssp-us-prior-art-c8-para-00011) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00012](#ssp-us-prior-art-c8-para-00012) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00015](#ssp-us-prior-art-c8-para-00015) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00017](#ssp-us-prior-art-c8-para-00017) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00018](#ssp-us-prior-art-c8-para-00018) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00020](#ssp-us-prior-art-c8-para-00020) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00021](#ssp-us-prior-art-c8-para-00021) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00023](#ssp-us-prior-art-c8-para-00023) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00027](#ssp-us-prior-art-c8-para-00027) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 3 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00030](#ssp-us-prior-art-c8-para-00030) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 4 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00033](#ssp-us-prior-art-c8-para-00033) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 5 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00036](#ssp-us-prior-art-c8-para-00036) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00037](#ssp-us-prior-art-c8-para-00037) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00038](#ssp-us-prior-art-c8-para-00038) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00039](#ssp-us-prior-art-c8-para-00039) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00040](#ssp-us-prior-art-c8-para-00040) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00041](#ssp-us-prior-art-c8-para-00041) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00042](#ssp-us-prior-art-c8-para-00042) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00046](#ssp-us-prior-art-c8-para-00046) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 7 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00049](#ssp-us-prior-art-c8-para-00049) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 8 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00052](#ssp-us-prior-art-c8-para-00052) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00053](#ssp-us-prior-art-c8-para-00053) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00054](#ssp-us-prior-art-c8-para-00054) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00055](#ssp-us-prior-art-c8-para-00055) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00056](#ssp-us-prior-art-c8-para-00056) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00060](#ssp-us-prior-art-c8-para-00060) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00066](#ssp-us-prior-art-c8-para-00066) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00078](#ssp-us-prior-art-c8-para-00078) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00084](#ssp-us-prior-art-c8-para-00084) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00091](#ssp-us-prior-art-c8-para-00091) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00098](#ssp-us-prior-art-c8-para-00098) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00106](#ssp-us-prior-art-c8-para-00106) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00117](#ssp-us-prior-art-c8-para-00117) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00132](#ssp-us-prior-art-c8-para-00132) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00135](#ssp-us-prior-art-c8-para-00135) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 19 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00142](#ssp-us-prior-art-c8-para-00142) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00145](#ssp-us-prior-art-c8-para-00145) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 21 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00149](#ssp-us-prior-art-c8-para-00149) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00155](#ssp-us-prior-art-c8-para-00155) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00157](#ssp-us-prior-art-c8-para-00157) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00164](#ssp-us-prior-art-c8-para-00164) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00167](#ssp-us-prior-art-c8-para-00167) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00169](#ssp-us-prior-art-c8-para-00169) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00170](#ssp-us-prior-art-c8-para-00170) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00171](#ssp-us-prior-art-c8-para-00171) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00172](#ssp-us-prior-art-c8-para-00172) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00173](#ssp-us-prior-art-c8-para-00173) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00174](#ssp-us-prior-art-c8-para-00174) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00176](#ssp-us-prior-art-c8-para-00176) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00177](#ssp-us-prior-art-c8-para-00177) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00178](#ssp-us-prior-art-c8-para-00178) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00179](#ssp-us-prior-art-c8-para-00179) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00180](#ssp-us-prior-art-c8-para-00180) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00182](#ssp-us-prior-art-c8-para-00182) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00183](#ssp-us-prior-art-c8-para-00183) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00184](#ssp-us-prior-art-c8-para-00184) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00185](#ssp-us-prior-art-c8-para-00185) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00189](#ssp-us-prior-art-c8-para-00189) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00190](#ssp-us-prior-art-c8-para-00190) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00191](#ssp-us-prior-art-c8-para-00191) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00192](#ssp-us-prior-art-c8-para-00192) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00193](#ssp-us-prior-art-c8-para-00193) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00194](#ssp-us-prior-art-c8-para-00194) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00198](#ssp-us-prior-art-c8-para-00198) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 27 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00210](#ssp-us-prior-art-c8-para-00210) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 28 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00217](#ssp-us-prior-art-c8-para-00217) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 29 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00220](#ssp-us-prior-art-c8-para-00220) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 30 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00221](#ssp-us-prior-art-c8-para-00221) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 30 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00225](#ssp-us-prior-art-c8-para-00225) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 31 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00228](#ssp-us-prior-art-c8-para-00228) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 32 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00229](#ssp-us-prior-art-c8-para-00229) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 32 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00233](#ssp-us-prior-art-c8-para-00233) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 33 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00234](#ssp-us-prior-art-c8-para-00234) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 33 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00235](#ssp-us-prior-art-c8-para-00235) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 33 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00236](#ssp-us-prior-art-c8-para-00236) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 33 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00240](#ssp-us-prior-art-c8-para-00240) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00241](#ssp-us-prior-art-c8-para-00241) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00242](#ssp-us-prior-art-c8-para-00242) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00243](#ssp-us-prior-art-c8-para-00243) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00244](#ssp-us-prior-art-c8-para-00244) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00245](#ssp-us-prior-art-c8-para-00245) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00247](#ssp-us-prior-art-c8-para-00247) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00248](#ssp-us-prior-art-c8-para-00248) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00249](#ssp-us-prior-art-c8-para-00249) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 34 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00258](#ssp-us-prior-art-c8-para-00258) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 35 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00261](#ssp-us-prior-art-c8-para-00261) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 36 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00264](#ssp-us-prior-art-c8-para-00264) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 37 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00267](#ssp-us-prior-art-c8-para-00267) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00268](#ssp-us-prior-art-c8-para-00268) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00269](#ssp-us-prior-art-c8-para-00269) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00270](#ssp-us-prior-art-c8-para-00270) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00271](#ssp-us-prior-art-c8-para-00271) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00272](#ssp-us-prior-art-c8-para-00272) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00273](#ssp-us-prior-art-c8-para-00273) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00275](#ssp-us-prior-art-c8-para-00275) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00277](#ssp-us-prior-art-c8-para-00277) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 38 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00281](#ssp-us-prior-art-c8-para-00281) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00282](#ssp-us-prior-art-c8-para-00282) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00284](#ssp-us-prior-art-c8-para-00284) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00286](#ssp-us-prior-art-c8-para-00286) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00288](#ssp-us-prior-art-c8-para-00288) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00290](#ssp-us-prior-art-c8-para-00290) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 39 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00301](#ssp-us-prior-art-c8-para-00301) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 40 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00304](#ssp-us-prior-art-c8-para-00304) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00305](#ssp-us-prior-art-c8-para-00305) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00306](#ssp-us-prior-art-c8-para-00306) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00307](#ssp-us-prior-art-c8-para-00307) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00308](#ssp-us-prior-art-c8-para-00308) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00309](#ssp-us-prior-art-c8-para-00309) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00312](#ssp-us-prior-art-c8-para-00312) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00315](#ssp-us-prior-art-c8-para-00315) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00316](#ssp-us-prior-art-c8-para-00316) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00317](#ssp-us-prior-art-c8-para-00317) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00319](#ssp-us-prior-art-c8-para-00319) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00321](#ssp-us-prior-art-c8-para-00321) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 41 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00325](#ssp-us-prior-art-c8-para-00325) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00326](#ssp-us-prior-art-c8-para-00326) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00327](#ssp-us-prior-art-c8-para-00327) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00328](#ssp-us-prior-art-c8-para-00328) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00329](#ssp-us-prior-art-c8-para-00329) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00330](#ssp-us-prior-art-c8-para-00330) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00331](#ssp-us-prior-art-c8-para-00331) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 42 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00335](#ssp-us-prior-art-c8-para-00335) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 43 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00337](#ssp-us-prior-art-c8-para-00337) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 43 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00341](#ssp-us-prior-art-c8-para-00341) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 44 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00344](#ssp-us-prior-art-c8-para-00344) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 45 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00345](#ssp-us-prior-art-c8-para-00345) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 45 | structured-transcription fragment | None declared |
| [us-prior-art-c8-para-00347](#ssp-us-prior-art-c8-para-00347) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 45 | structured-transcription fragment | None declared |
| [us-prior-art-c8-plain-00081](#ssp-us-prior-art-c8-plain-00081) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c8-plain-00109](#ssp-us-prior-art-c8-plain-00109) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c8-plain-00114](#ssp-us-prior-art-c8-plain-00114) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-plain-00120](#ssp-us-prior-art-c8-plain-00120) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-plain-00122](#ssp-us-prior-art-c8-plain-00122) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-plain-00124](#ssp-us-prior-art-c8-plain-00124) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c8-rawblock-00156](#ssp-us-prior-art-c8-rawblock-00156) | US/prior-art/C8/C8\_ETSI-TS-104-002\_DASH-IF-AB-Watermarking.pdf | 23 | structured-transcription fragment | None declared |
