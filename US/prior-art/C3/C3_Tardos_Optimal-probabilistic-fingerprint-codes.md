<!-- GENERATED REVIEW PROJECTION — source us-prior-art-c3; byte digest sha256/raw:d64b1d36b23b641e1162df3c822055bce0945761c87b0416eb7bf7677b6ddaf1; source profile pdf-evidence-transcription-v1; projection profile gfm-v1/generated-v1; regenerate with `uv --no-cache --offline run --locked --no-sync python -m structured_source regenerate us-prior-art-c3`; edit the XML source, never this Markdown. -->
<a id="ssp-us-prior-art-c3-root"></a>

<a id="ssp-us-prior-art-c3-header-00001"></a>
# C3 — Tardos, “Optimal Probabilistic Fingerprint Codes” — author-hosted extended version of the STOC 2003 paper

<a id="ssp-us-prior-art-c3-blockquote-00002"></a>
> <a id="ssp-us-prior-art-c3-para-00003"></a>
> **WORKING TRANSCRIPTION — NOT AN OFFICIAL COPY AND NOT FOR FILING.**
>
> <a id="ssp-us-prior-art-c3-para-00004"></a>
> Source: `C3_Tardos_Optimal-probabilistic-fingerprint-codes.pdf`. Working transcription produced with OCR from the stored PDF. Verify every quotation, number, date, and reference numeral against the stored PDF; the co-located source manifest records its current evidence binding.
>
> <a id="ssp-us-prior-art-c3-para-00005"></a>
> Text-layer extraction: characters are the publisher's own, not inferred. Reading order is reconstructed from line geometry, so paragraph flow across page and column breaks — and table alignment — still needs visual confirmation against the PDF. Line-number artifacts (5, 10, 15 …) may remain mid-sentence.

<a id="ssp-us-prior-art-c3-horizontalrule-00006"></a>

---

<a id="ssp-us-prior-art-c3-header-00007"></a>
### Page 1

<a id="ssp-us-prior-art-c3-para-00008"></a>
Optimal
G´abor
R´enyi
Pf.127,H-1354
Weconstructbinarycodesfor
codes for n users that are ǫ-secure against
Thisimprovesthecodesproposed
isapproximatelythesquareofthis
toworksusingtheBoneh-Shaw
traitortracingschemeofTassa\[16\].
Byprovingmatchinglower
codesisbestwithinaconstant
Thislowerboundgeneralizesthe
Shelat,and Smith \[11\] that applies to a limited class
alsoimplythatrandomizedﬁngerprint
aspowerfulasoveranarbitrary
distinctmodelsforﬁngerprinting.
Introduction
1.1
Motivation
somethinglikeaserialnumberisa
speciﬁccustomer(user)whobought
includecopyrighted digitaldocuments
video.Leakingsensitivedocumentsto
Iftheusersdonotcheat,this
may tryto erase theserial number (also called
distributingillegalcopies.Toprevent
∗Preliminaryversionofthispaperappeared
beensupportedbytheHungarianNational
theHungarianScienceFoundationgrants
AKP2000-782.1.
Probabilistic FingerprintCodes∗
Tardos
Institute
Budapest,Hungary
[tardos\@renyi\.hu](mailto:tardos@renyi.hu)
Abstract
ﬁngerprintingdigitaldocuments.Our
c pirates have length O(c2log(n/ǫ)).
byBonehandShaw\[3\]whoselength
length.Theimprovementcarriesover
codeasaprimitive,e.g.tothedynamic
bounds weestablishthatthe lengthofour
factorforreasonableerrorprobabilities.
boundfoundindependentlybyPeikert,
of codes.Our results
codesoverabinaryalphabetare
alphabetandtheequalstrengthoftwo
The problem of making many copies of a digital document unique by embedding
verynaturalone.Forexample,asoftware
distributor may want to be able to trace any running copy of his software to the
thatpieceofsoftware.Otherapplications
of anyform,e.g.digitalimages,audioor
thepresscanalsobefoughtthisway.
representsnoproblem,butamalicioususer
ﬁngerprint) from hiscopy before
suchfrauditisnaturaltodistributethe
digits of the ﬁngerprint into locations of the digital document that are unknown
inSTOC’03\[15\].Workonthispaperhas
Research&DevelopmentFund\#2/019/2001,
OTKAT029255,OTKAT030059,andthegrant

<a id="ssp-us-prior-art-c3-horizontalrule-00009"></a>

---

<a id="ssp-us-prior-art-c3-header-00010"></a>
### Page 2

<a id="ssp-us-prior-art-c3-para-00011"></a>
to the users.
digitsareonthesepositions),butthe
ﬁnd for theuser.This way the
alteringrelevantdigitsofthedocument
asasequenceofdigits.Inthispaper
digitsoftheﬁngerprint.Thisisahighly
Afurtherproblemariseswhena
pirates)collaborate.Eachofthemhas
document.Comparingthesecopies,
copies diﬀer,thesepositions hold digits
digitsoftheﬁngerprintortheycan
positions.
Suchastrategyresultsin
identicaltoanyofthelegitimate
ofthemonrelevantpositions.Inthis
abletoidentifyatleastonepirateof
piratesdonotalterthedigitaldocument
theyseeagree.Thisiscalledthe
anarbitrarystrategytoﬁllinthe
(SeeSection6foraslightrelaxation
Itisimportantthatinthescenario
digit in the document on positions where they detected diﬀerence.
thepiratestouseadigitatany
inoneoftheirdocuments,weget
thepiratesifthealphabetisnot
deterministicsolution,suchcodesare
assumption(whileadequateinsome
manyﬁngerprintingapplications.Our
freesolutionifthereareatleastthree
pirate coalition.
ofrelatedresultsinSection1.3.
1.2
TheModel
Since a deterministic solution does not exist,
togeneratecodewordsandaccuse
theformaldeﬁnitionbelow,wesimplify
positions of the document and concentrating on the
lengthoftheﬁngerprintcodeisthe
embedsuchacode.
Deﬁnition1.1.Aﬁngerprintcode
Σisadistributionoverthepairs(X, σ
andσisanalgorithmthattakesa
andproducesasubsetσ(y) ⊆\[n\] := \{
∅̸ = C⊆\[n\] a C-strategy is an algorithm
The digits in these positions must be irrelevant with respect to the
intended use of the document (e.g. the software must run correctly whatever the
exactlocationsshouldbeimpossibleto
user cannot erase theﬁngerprint without risking
too.Hereweconsiderthedocument
wedonotconsiderthetaskofhidingthe
nontrivialimplementationchallenge.
coalitionofmalicioususers(wecallthem
accesstooneﬁngerprintedcopyofthe
theycanidentifythepositionswherethe
of theﬁngerprint.Theycan erase these
evenintroducearbitrarydigitsinthese
adocument(piratedcopy)thatisnot
(ﬁngerprinted)copiesbutisidenticalwithall
scenario,wewantthedistributortobe
theguiltycoalition.Weassumethatthe
onpositionswhereallofthecopies
markingcondition.Thepiratesmayhave
positionswheretheydetecteddisagreement.
ofthemarkingcondition.)
weconsiderthepiratescanputany
If we restrict
positionthatappearsinthesameposition
anothermodelthatismorerestrictivefor
binary.
Thisalternatemodelallowsfora
calledIPPcodes.Thismorerestrictive
applications)seemstobetoostrongin
problemformulatedabovehasnoerrorusersandanytwoofthemcanformthe
We present here an eﬃcient randomized scheme.See discussion
we turn to a randomizedprocedure
usersthatworkswithhighprobability.In
thenotationbyignoringtherelevant
ﬁngerprint itself.Thus,the
numberofirrelevantpositionsneededto
oflengthmfornusersoverthealphabet
),whereXisannbymmatrixoverΣ
stringy∈Σm(thepiratedcopy)asinput,
1, 2, . . ., n\}(thesetofaccusedusers).For
ρ that takes the submatrix of Xformed

<a id="ssp-us-prior-art-c3-horizontalrule-00012"></a>

---

<a id="ssp-us-prior-art-c3-header-00013"></a>
### Page 3

<a id="ssp-us-prior-art-c3-para-00014"></a>
bytherowswithindicesinCasinput,
asoutput1andsatisﬁesthemarking condition
ifallthevaluesXjiforj∈Cagree
thataﬁngerprintcodeisǫ-secure against
ofsize\|C\| ≤candforanyC-strategy
P\[σ(ρ(X)) = ∅
isatmostǫ.
Ourmainresultsareaconstruction
lary3)andamatchinglowerbound
Theorem4).Westatetheseresults
section.
Remarks
1.
algorithms σand ρ.
algorithms.Randomization in σ
whileforρonecansupposeitchooses
maximizes theerror probability.Thus,
algorithms here (or simply considering
lentdeﬁnitions.Weassumeallalgorithms
stated.
the next section uses a very eﬃcient algorithm
by a linear constraint.
isalsobasedonverysimple(randomized)
2.In the setting of the above deﬁnition,
userisaccused,i.e.,that\|σ(y)\|=1.
oneuserfromthesetσ(y)andan
increasetheerrorprobability.However,
ofaccusinganinnocentuserandthe
obviousreasonstheformertypeof
consideredfarworse.Ourconstruction
thesoundnesserrorismaintainedeven
achievethisthealgorithmσneedsto
sure.
3.Thedeﬁnitionaboveassumes
advance.Ourconstructionhowever
canbegeneratedonebyoneasusers
4.Intherealscenarioofﬁngerprinting
thedeﬁnition,thepirateshavejusta
ofthisdeﬁnition.
Indeed,theylearn
notalloftheircodesagree.Thus,
consistingoftheirrespectiverows,
1Forsimplicity,wedenotetheoutputof
theinputisonlyasubmatrixofX,ρ“does
andproducesastringy=ρ(X)∈Σm
that,forallpositions1 ≤i ≤m,
withsomeletters ∈Σthenyi= s.Wesay
coalitionsofsizec,ifforanyC⊆\[n\]
ρ,theerrorprobability
orσ(ρ(X))̸ ⊆C\]
ofshortﬁngerprintcodes(seeCorolforthelengthofanyﬁngerprintcode(see
andgivetheconstructionitselfinthenext
In the above deﬁnition, we do not have any complexity assumptions on the
Furthermore, we can restrict our attention to deterministic
can be “moved” to the distribution over (X, σ),
deterministicallyoneofthestringsthat
considering randomized or deterministic
σand ρ to befunctions) leads to equivatobedeterministicunlessotherwise
Despite allowing algorithms of arbitrary complexity, our construction in
σ:each accusation is determined
The proof of the lower bound claimed in the next section
algorithmsρ.
one can assume that always a single
Indeed,onecanmodifyσtoaccuseany
arbitraryuserifσ(y)=∅.Thisdoesnot
laterwewilltreatseparatelytheerror
errorofnotaccusinganyguiltyone.For
error(thatwecall“soundnesserror”)is
hastheadvantagethattheboundon
againstarbitrarilylargecoalitions.To
beablenottoaccuseanybodyifitisnot
thatthenumbernofusersisknownin
doesnotneedthisassumption:codewords
appear.
digitaldocumentsexplainedbefore
littlelessinformationthaninthesetting
onlyaboutirrelevantpositionswhere
theycanreconstructthesubmatrixofX
butmissingallcolumnsthatareconstant
theC-strategyρbyρ(X),despitethefactthat
notsee”therowswithindicesoutsideC.

<a id="ssp-us-prior-art-c3-horizontalrule-00015"></a>

---

<a id="ssp-us-prior-art-c3-header-00016"></a>
### Page 4

<a id="ssp-us-prior-art-c3-para-00017"></a>
inthissubmatrix.
Thissubtle
ourconstructionissecureagainst
also,ourlowerboundworksinthis
based on very simplestrategies ρ
depends(in somerandomized manner) only
codewords(theithcolumnofthe
1.3
EarlierResults
Fingerprinting was ﬁrst studied by Wagner \[18\].
piratecoalitionswasstudiedbyBlakley
ﬁngerprintingarestudiedinthe
amodelwheretheﬁngerprintcanalter
bebounded.
IPPoridentiﬁableparentproperty
Thesecodesmustworkonlyagainst
suchthatforanyitheithposition
positionofalegitimatecopythepirates
relatedtraitortracingarewidely
alreadymentioned,thismorerestrictive
manyﬁngerprintingapplications.
moreappropriateintermediatemodel.
acomparisonbetweenthesemodels.
Thefollowingisthestandard
thepiratescouldintroducearbitrary
apiratecoalition.Consideranythree
distributedtotheplayersandletX
iiftheithdigitsofatleasttwoofX
theithdigitofXisalsos.(Overthe
X2andX3,itistheirbitwisemajority.
determineduniquelybyXjbutsuch
ofthethreeusersformthepirate
withthepiratedcopyy=X.Thus
ofthemforproducingthiscopywithout
arelatedmodelChung,Graham,and
acceptingaccusationsoftheform
andevenmorecomplicatedaccusations
modeltheystudythecodelengthmust
Randomized ﬁngerprint codes
ﬁngerprintcodetheyproposeuses
ﬁrstdeterministicallyconstructacode
randomlypermutingthecolumnsof
thefullpowerofrandomizationallowed
constructedﬁngerprintcodesoflength
ǫ-secureagainstcoalitionsofanysize.
diﬀerenceisnotrelevantthough.
Naturally,
thesemorerestrictedpiratecoalitions,and
morerestrictedcasetoo,astheproofis
for cheating,where theith digit of theoutput
on theith digitsoftheirrespective
submatrix).
Fingerprinting resilient against
etal.\[1\].Manydiﬀerentmodelsfor
literature.SeeforexampleKilianetal.\[8\]for
thedocumentbutthedistanceshould
codeswereintroducedbyChoretal.\[4\].
pirateswhomustoutputapiratedcopy
ofthepiratedcopyisidenticaltotheith
haveaccessto.Thesecodesandthe
studied,seee.g.\[2,9,13,14\].Aswehave
assumptionseemstobetoostrongin
Theunreadabledigitmodelseemstobea
SeeSection5forthedeﬁnitionandfor
argumenttoshowthatinourmodel,where
digitsinpositionstheircodewordsdiﬀer,
no deterministic ﬁngerprint code exists for 3 players if any two of them can form
ﬁngerprinteddocumentX1,X2andX3
beadocumentsuchthatforanyposition
1,X2andX3aresomeletters∈Σthen
binaryalphabetXisdeterminedbyX1,
OverlargeralphabetsXmaynotbe
Xalwaysexist.)Nomatterwhichtwo
coalitionitispossibleforthemtocomeup
nodeterministicalgorithmcanaccuseany
riskingaccusinganinnocentuser.(In
Leighton\[5\]getaroundthisproblemby
“twooutofthesethreeplayersareguilty”
forlargercoalitions.Buteveninthe
beexponentialinthecoalitionsize.)
were introducedbyBoneh and Shaw\[3\].The
randomizationinarestrictedway.
They
matrixanduserandomizationonlyfor
thismatrix.We,ontheotherhand,use
byDeﬁnition1.1.BonehandShaw
m = O(n3log(n/ǫ))fornusersthatare
Againstcoalitionsofsizec\<nthey

<a id="ssp-us-prior-art-c3-horizontalrule-00018"></a>

---

<a id="ssp-us-prior-art-c3-header-00019"></a>
### Page 5

<a id="ssp-us-prior-art-c3-para-00020"></a>
constructedǫ-secureﬁngerprintcodes
nusers.Infollow-upworksLindkvist
lengthnoteﬀectingtheasymptotics,
implementation of theBoneh-Shaw codes.
thenextsectionisapproximatelythe
Shawcodes.
Dynamictraitortracingwas
originallyadeterministicmodelrequiring
\[16\]introducedamoreeﬃcient
Shaw code as a primitive in his scheme.
nextsectionsubstantiallyimprovesthe
BonehandShawalsoproveanΩ(
ofﬁngerprintcodes.Ourlowerbound
matchestheconstructionifǫis
\[11\]prove alower boundfora
isbasicallythesameasourboundin
withalimitednumberof“column
diﬀertheirsideconditiononthenumber
thattheoriginal construction of Boneh and
constructedinthispaperdonotsatisfy
theirboundstoapply.Nevertheless,
c2log(1/ǫ)bound.Thepiratestrategy
ourstrategy,botharebasedona
Therestofthepaperisorganized as
ourconstructionforﬁngerprintcodes
3and4weproveTheorems1and2,
favorablepropertiesofourﬁngerprint
unreadable digitmodel
inthestandard(arbitrarydigit)model
proveourlowerboundresult(Theorem
ouroriginallowerbound(Theorem4)
lengthoftheconstructioninthe
weakerestablishestheequalstrength
strengthofﬁngerprintcodesoverbinary
ofthislowerbound.Section6contains
Constructionand
Our main result is the construction of ﬁngerprint codes of length
thatareǫ-secureagainstcoalitionsof
ingtheconstructionwemotivatesome
thenstateitsmainpropertiesin
strongerthantherequirementsof
addedadvantagesofourcodesfollow.
oflengthm = O(c4log(1/ǫ) log(n/ǫ))for
\[10\]mademinorimprovementonthe
whileYacobi\[17\]designedaveryeﬃcient
The length of our codes presented in
squarerootofthelengthoftheBonehintroducedbyFiatandTassa\[6\].Thiswas
highalphabetsize,butTamirTassa
probabilisticversion.TassausestheBonehSubstitutingour codes presented in the
convergencetimeoftheTassascheme.
c log(1/(cǫ)))lowerboundforthelength
improvestheirboundsigniﬁcantlyand
reasonablysmall.Peikert,Shelat,andSmith
restricted typeof ﬁngerprint codes.Theirbound
Theorem4,butitonlyappliesforcodes
types”.IfallcolumnsofthecodematrixX
ofcolumntypesisnotmet.Forcodes
that use randomization in the limited way the Boneh-Show code does they prove
Showisalmost optimal.Thecodes
therequirementsneededforeitherof
theresultsin\[11\]alsopointtowardthe
theyemployintheproofissimilarto
carefullyselectedbiasfunction.
follows.Inthenextsection wepresent
andsummarizeourresults.InSections
respectively,thetworesultsstatingthe
code.
InSection5weintroducethe
for ﬁngerprinting, and we prove that any ﬁngerprint code
alsoworksinthismodel.Westateand
5)fortheunreadabledigitmodel,and
followsasaconsequence.Thematching
strongermodelandthelowerboundinthe
ofthetwomodels.Similarly,theequal
andlargeralphabetsisaconsequence
afewconcludingremarks.
Results
m = O(c2log(n/ǫ))
sizec(seeCorollary3).Afterpresentoftheseeminglyarbitrarychoicesinit,
Theorems1and2.Theseresultsaremuch
Deﬁnition1.1.
Afewcommentsonthese
Theorem4statesalowerboundforthe

<a id="ssp-us-prior-art-c3-horizontalrule-00021"></a>

---

<a id="ssp-us-prior-art-c3-header-00022"></a>
### Page 6

<a id="ssp-us-prior-art-c3-para-00023"></a>
lengthofﬁngerprintcodesthatmatches
isreasonablysmall.
2.1
TheConstruction
Inthispaper,logalwaysdenotesthe
Let n and c be positive integers, 0
thebinaryﬁngerprintcodeFncǫof
followingdistributionoverthepairs(
Weselectthepair(X, σ)intwo
ticallydistributedrandomvariables
t=1/(300c)andpi=sin2riisselected
valueri∈\[t′, π/2 −t′\]with0 \< t′\< π/
Inthesecondphase,weselectthe
Xjiindependently from the binary alphabet
that independenceof theentries Xji
randomvariablesXjiandXj′iare
tobe1ifpiislarge.
Theaccusationalgorithmσis
X,asfollows.Wedeﬁnethenbym

q


Uji=
q
−


Letσaccuseuserjonthepirated
m
X
yi
i=1
whereZ=20ckisathresholdparameter.
indicesjforwhichthejthentryofUy
RemarksHavingdescribedthe
choicesinit.
TheformuladeﬁningUjiischosen
dependsonXji,itispositiveifXji=
1.Foramotivationobservethathaving
makes player jmore suspicious if Xji
havinga1inthepiratedposition
issmall)makestheseplayersevenmore
Our choice of the distribution for p
(as opposed to values close to 1/2).
to these columns with a high bias.
totallywithouthighlymixedcolumns,
lowerboundonthelengthofﬁngerprint
ourconstructioniftheerrorboundǫ
naturallogarithm.
\< ǫ \< 1 and let k= ⌈log(1/ǫ)⌉.We deﬁne
lengthm=100c2kfornuserstobethe
X, σ).
phases.First,letpibeindependent,idenfrom\[t, 1−t\]forall1≤i≤m.
Here
bypickinguniformlyatrandomthe
4,sin2t′= t.
codematrixX,byselectingeachentry
\{0, 1\} with P\[Xji= 1\] = pi.Notice
holdsonlyin thesecond phase,theoverall
positivelycorrelatedasbothofthemtend
determinedbythevaluespiandthematrix
matrixUwithentries
−pi
ifXji= 1,
pi
pi
1−piifXji= 0.
copyy∈\{0, 1\}masinputif
Uji\> Z,
Inotherwords,σ(y)consistsofthe
TexceedsZ.
constructionherewemotivatesomeofour
sothataftertheﬁrstphase,itonly
1andithasexpectation0andvariance
1astheithdigitinthepiratedcopy
= 1 and less suspicious otherwise.Clearly,
whereonlyafewplayershavethatdigit(pi
suspicious.
i is biased toward the values close to 0 or 1
This is motivated by the marking condition.
This is the only restriction on the pirates’ strategy and it is more likely to apply
On the other hand, no ﬁngerprint code can do
thisisthebasicideaoftheBoneh-Shaw
codes.

<a id="ssp-us-prior-art-c3-horizontalrule-00024"></a>

---

<a id="ssp-us-prior-art-c3-header-00025"></a>
### Page 7

<a id="ssp-us-prior-art-c3-para-00026"></a>
Technically,thechoiceofthe
“completeness”(Theorem2)toshow
onlyaminoreﬀecton(anexponential
caught.
Thecutoﬀpointstand1 −tfor
technicalreasons.Ifpigetstooclose
highapositiveornegativevalue
muchofaninﬂuenceovertheaccusations.
Thefollowingtwotheoremsbound
Theorem1boundsthe“soundness
Theorem 2 bounds the “completeness error” of not accusing any guilty one.
boththeoremsn ≥c ≥1and0 \< ǫ \<
Theorem1.Let(X, σ)bedistributed
arbitraryuser,letC⊆\[n\] \\ \{j\}bea
andletρbeanyC-strategy.Wehave
P\[j∈σ
Theorem2.Let(X, σ)bedistributed
coalitionofsize\|C\| ≤c,andletρbe
P\[C ∩σ(ρ(
2.2
Advantagesofthe
strongerthenthoserequiredbythe
orem1statesthatinnocentusersare
userscollaborateagainstthem.As
markingcondition,innocentusersare
ratescanﬁndthepositionsofthe
marking condition.In other words, we
userisamemberofthegroupofpirates
thesizeorpowerofthisgroup.Our
thatFncǫ(oranyﬁngerprintcodeof
coalitionsofsizemuchlargerthanc.
theyareabletocomeupwithastrategy,
isaccused.AsTheorem1stillapplies,
tributorcanusethispropertythe
forc,assumesthatatmostcusers
Fncǫ.Any user the code accuses will likely to be
ofthedistributor’sassumption.If
thisindicatesthatthepiratecoalition
markingcondition).
distributionofpiisusedonlyintheproofof
thatthepirates’choiceofstrategyhas
averagerelatedto)theirchancetobe
thedistributiononpiareintroducedfor
toeither0or1thenUjicanhavetoo
and thereforethissinglepositioncanhave too
theerror probabilitiesofourcodesFncǫ.
error”ofaccusinganinnocentuser,while
For
1arearbitrary.
accordingtoFncǫ.Letj∈\[n\]bean
coalitionofarbitrarysizenotcontainingj,
(ρ(X))\] \< ǫ.
accordingtoFncǫ.LetC⊆\[n\]bea
anyC-strategy.Wehave
X)) = ∅\] \< ǫc/4.
Construction
Notice that Theorems 1 and 2 establish properties that are in most parts, much
deﬁnitionofǫ-security.Mostnotably,Thenotlikelytobeaccusedevenifallother
theproofofTheorem1doesnotusethe
notlikelytobeaccusedevenifthepiﬁngerprintcodeandthustheycanbreakthe
can bereasonably sure that any accused
evenifwedonotknowanyboundon
lowerboundtheorem(Theorem4)tellsus
thesamelength)cannotbesecureagainst
Ifmuchmorethancuserscollaborate,
sothatinalllikelihoodnoneofthem
inthiscasenobodyisaccused.Thedisfollowingway.Hechooses areasonable value
collaborateandusestheﬁngerprintcode
guilty regardless of the validity
theaccusationalgorithmaccusesnobody,
islargerthanc(ortheycanbreakthe

<a id="ssp-us-prior-art-c3-horizontalrule-00027"></a>

---

<a id="ssp-us-prior-art-c3-header-00028"></a>
### Page 8

<a id="ssp-us-prior-art-c3-para-00029"></a>
Anotheradvantage of thiscodeis
compute σ(y) one only has to multiply
entriesoftheresultingvectorexceed
Noticethatthedistributordoes
onlyoncandǫ,onecanﬁndthelength
accordingtotherequireddistribution.
Thenextphasecanbecarriedout
Wheneveranewusercomesup,the
corresponding row of the matrix X
asthecorrespondingrowofthematrix
Theorem2isstrongerthanrequired
Thisisonlyoftheoreticalinterestas
higherandthattypeoferrorisconsidered
AneasytoﬁxweaknessofTheorem
accusing a single innocent user and not the probability of accusing
users.Thisisanaturalconsequence
doesnotdependonthenumberof
usersmustsharetheircodewordwith
piratedistributinghiscopyisimpossible
FromTheorems1and2itclearly
Corollary3.TheﬁngerprintcodeF
ifc ≥4.ThelengthofthiscodeisO(
2.3
TheLowerBound
Theorem4.LetFbeaﬁngerprint
Σfornusers.Let3 ≤c ≤nbean
a \> 1isaconstant.IfFsatisﬁes
m ≥da
whereda\> 0dependssolelyona.
(i)ForanycoalitionC⊂\[n\]ofsize
anyuserj∈\[n\] \\ C,wehave
P\[j∈
(ii)ForanycoalitionC⊆\[n\]ofsize
have
P\[C ∩σ(
WhileTheorems1and2claim
an ǫ-secureﬁngerprint code,ourlower
ertiesofthecodethataresomewhat
codes.
ComparingtheresultsofTheorems1,
thesimplealgorithm σforaccusation.To
ywith a ﬁxed matrix Uand check which
athresholdparameterZ.
notneedtoknowninadvance.
Based
mofthecodeandselectthevaluespi
Thisistheﬁrst(preprocessing)phase.
separately(independently)foreachuser.
distributorcan generatehiscodeword (the
) and the rules for his accusation will be clear
Uisalsodeﬁned.
initsboundontheerrorprobability.
the“soundnesserror”ofTheorem1is
worse.
1isthatitboundstheprobabilityof
some innocent
ofthefactthatthelengthofthecodem
users.Ifnislargerthan2m+1,thenmost
anotheruser.Inthiscaseevenasingle
tocatch withoutahigh riskof failure.
followsthat
ncǫ
nisǫ-secureagainstcoalitionsofsizec
c2log(n/ǫ)).
codeoflengthmoveranarbitraryalphabet
integerand0 \< ǫ \< 1/(100ca)areal,where
conditions(i)and(ii)belowthen
c2log(1/ǫ),
\|C\| = c −1,foranyC-strategyρ,andfor
σ(ρ(X))\] ≤ǫ.
\|C\|=c,andforanyC-strategyρ,we
ρ(X)) = ∅\] \< 0.99.
propertiesmuchstrongerthanrequiredfor
boundresult,Theorem 4,assumespropweakerthenthoserequiredforǫ-secure
This makes the matching lower and upper bounds even more interesting.
2,and4onecannoticethefollowing.

<a id="ssp-us-prior-art-c3-horizontalrule-00030"></a>

---

<a id="ssp-us-prior-art-c3-header-00031"></a>
### Page 9

<a id="ssp-us-prior-art-c3-para-00032"></a>
1.The length of our codes Fncǫ
codessatisfyingtheconditionsof
ByCorollary 3,thelengthofthecode
amongstallcodesfornusersthat
ǫ \< 1/(100ca)foraﬁxeda \> 1andǫ \<
on ǫ seems to be reasonable, as in case
independently with probability ǫ
withcodelengthm=0.Seefurther
Section6.
2.
Betweenthetwotypesoferror
hasmoreeﬀectonthecodelength
ofaccusinginnocentusers.The
accusinganyofthepirates,canbe
withouthavingasigniﬁcanteﬀecton
completeness error vanish entirely seems to be diﬃcult though.
thatwouldmixsomeofthedeterministic
probabilisticpropertiesoftheBoneh-Shaw
3.OurcodesFncǫarebinary,and
arbitrary alphabets.
codesareasgoodforﬁngerprinting
gives the same answer but only for a very limited class of ﬁngerprint codes.
resultisinsharpcontrastwithIPP
donotexistoverabinaryalphabet.
4.InSection5,weintroduceanother
abledigitmodel,inwhichthepirates
illegitimatecopyρ(X).Inthismodel
inthepositionsoftheillegitimatecopy
theycannotputaspeciﬁcdigitnone
Theorems1and2remaintruein
againstthesemorerestrictedpirate
statement).Weprovethelowerbound
digitmodel(seeTheorem5)andget
thattheunreadabledigitmodeland
almostequivalentwithrespectto
factcomesfromcertainapplications
tobemore natural.If“digits”are
safelyassumethatthepiratescannot
documentscontains,buttheycan
theydetecteddisagreement.Forthe
unreadabledigit.
5.Theconstant0.99inTheorem
1 −νinplaceof0.99ifǫ \< (ν/c)afor
wecanhaveacodeoflengthm=0:
probabilityatmostǫ.
are optimal within a constant factor amongst
Theorem4ifǫ \< 1/(100ca)foraﬁxeda \> 1.
Fncǫ
nisoptimalwithinaconstant factor
areǫ-secureagainstcoalitionsofsizecif
1/nbforaﬁxedb \> 0.Theassumption
ǫ ≥1/c, one can simply accuse everybody
and both conditions of Theorem 4 are satisﬁed
remarksonǫ-securecodeswithhighǫin
probabilities,theimportantonethat
isthe“soundnesserror”,theprobability
“completenesserror”,theprobabilityofnot
arbitrarilychoseninaverywideinterval
theoptimalcodelength.
Makingthe
A code achieving
featuresoftheIPPcodeswiththe
codesandthecodesofthispaper.
haveoptimallengthamongstcodesover
This answers the problem raised by Lindkvist \[10\] if binary
ascodesoverlargeralphabets.Lindkvist
This
codesthatexistoverlargeralphabets,but
modelforﬁngerprinting,theunreadaremorerestrictedinproducingtheir
thepiratescanput“unreadabledigits”
wheretheydetecteddisagreementbut
ofthemhasinthatposition.Naturally,
thismodel(thecodeFncǫremainssecure
coalitions;seeLemma5.3fortheprecise
statedinTheorem4intheunreadable
Theorem4asacorollary.Thus,weprove
themodelconsideredinthissectionare
optimalcodelength.Theimportanceofthis
wheretheunreadabledigitmodelseems
implementedascomplicated objects,wecan
createwell-formeddigitsnoneoftheir
simplyputrandomnoiseinpositionswhere
distributorthisrandomnoisewillbean
4isarbitrary.Ourtechniquesworkwith
someconstanta \> 1.Forn = c,ǫ = ν/c
simplyaccusearandomuser,eachwith

<a id="ssp-us-prior-art-c3-horizontalrule-00033"></a>

---

<a id="ssp-us-prior-art-c3-header-00034"></a>
### Page 10

<a id="ssp-us-prior-art-c3-para-00035"></a>
WhytheInnocent
Provingthatourﬁngerprintcodeworks
InthissectionweproveTheorem1,
likelytobeaccused.
ProofofTheorem1:Letn,c,ǫ,
j/∈Cwecanconsiderperforming
Fncǫcodes(i.e.,selectingthevaluesp
j∈C(i.e.,selectingtherowsofX
beforeselectingrowjofX.Thisway
ofplayerjisselected.Weclaimthat
eventj∈σ(ρ(X))boundedbyǫ,but
ytheprobabilityofj∈σ(y)isbounded
statementprovesthetheorem.
Wehaveﬁxedvaluespifrom\[t, 1
choose Xjifrom \{0, 1\} independently
p
(1 −pi)/piifXji
Recallthatui=
FinallywesetS=Pm
i:yi
i=1yiui=P
S\> Z,soweneedtoprovethatP\[S
ConsidertheexpectedvalueE\[eαS
rithm,andα = 1/(10c).Usingthe
have


<a id="ssp-us-prior-art-c3-para-00036"></a>
= E
E
eαS
Y
i:yi=1
Next we use 1+u ≤eu≤1+u+u2
thesecondinequalityholdsforu\<1
andthusαui\< 1.Usingthatuihas
E \[eαui\] ≤E
= 1 + αE \[ui\] + α2
Y

<a id="ssp-us-prior-art-c3-header-00037"></a>
# E \[eαui

<a id="ssp-us-prior-art-c3-para-00038"></a>
E
eαS
i:yi=1
FinallybytheMarkovinequalitywe

<a id="ssp-us-prior-art-c3-para-00039"></a>
P\[S\> Z\] = P
eαS\> e
Heretheexponentisα2m −αZ= −k
P\[S\> Z
asclaimed.
IsNotAccused
consistsofprovingTheorems1and2.
establishingthatinnocentusersarenot
j,C,andρbeasinthetheorem.As
theﬁrstphaseoftheconstructionofthe
i),performingthesecondphaseforrows
seenbyρ),andrunningthealgorithmρall
y=ρ(X)isﬁxedbeforethecodeword
notonlyistheoverallprobabilityofthe
conditionedonanysetofvaluespiand
byǫ.Clearly,provingthisstronger
−t\]andaﬁxedstringy∈\{0, 1\}m.We
with P\[Xji= 1\] = piand deﬁne ui= Uji.
p
=1andui=−
pi/(1 −pi)ifXji=0.
=1ui.Userjisaccused(i.e.,j∈σ(y))if

<a id="ssp-us-prior-art-c3-blockquote-00040"></a>
> <a id="ssp-us-prior-art-c3-para-00041"></a>
> Z\] \< ǫ.
> \]whereeisthebaseofthenaturallogaindependenceoftherandom variablesuiwe
> 
> Y
> E \[eαui\] .
> eαui
> =
> i:yi=1
> , where the ﬁrst inequality always holds, and
> p
> .7.Noticethatui≤
> (1 −t)/t≤t−1/2
> expectationzeroandvariance1weget

<a id="ssp-us-prior-art-c3-para-00042"></a>
1 + αui + α2u2
i

<a id="ssp-us-prior-art-c3-para-00043"></a>
= 1 + α2≤eα2.
E
u2
i

<a id="ssp-us-prior-art-c3-para-00044"></a>
≤eα2m.
\] ≤
eα2\|\{i:yi=1\}\|
have

<a id="ssp-us-prior-art-c3-para-00045"></a>
eαS
αZ
≤eα2m−αZ.
\<E
eαZ
= −⌈log(1/ǫ)⌉thus
\] \< e−k≤ǫ

<a id="ssp-us-prior-art-c3-horizontalrule-00046"></a>

---

<a id="ssp-us-prior-art-c3-header-00047"></a>
### Page 11

<a id="ssp-us-prior-art-c3-para-00048"></a>
WhySomePirateIs
InthissectionweturntoTheorem2
oneofthepirateswithveryhigh
ProofofTheorem2:Letn,c,ǫ,C
withoutlossofgeneralitythatC=
outsideCareirrelevant.Let(X, σ)
HereσisdeterminedbyXand
p=
p
qi=
(1 −pi)/piandrecallthe
ifXji= 0.Letussety= ρ(X)andS
m
X
X
S=
Sj=
i=1
j∈C
where xi=Pn
j=1Xjidenotes the
j∈Cisaccused(i.e.,j∈σ(y))ifSj
inCmustbeaccused.Itisenoughto
P\[C ∩σ(ρ(X
Thehighleveldescriptionofthe
beabletoproducey=ρ(X)consisting
andinparticularouralgorithmσwould
pirates,forindicesisuchthatcolumn
outputyi=1bythemarkingcondition,
may try to oﬀset this increase by outputting some ones at indices
iofXismixed.Byoutputting1they
thantheexpectednumberofpinones,
morethanthatmanyones.They
buttheydonotknowpi.Wechose
andthelossesalmostcanceloutand
theexpectationofS(moreprecisely
suitable α).Theincrease coming from the
oﬀset,anditisenoughtomakeS\> nZ
Wesetα = 1/(20c).Intheﬁrst
average E\[e−αS
C-strategy ρ.In thesecond part of the
establishthatthetwoformulaeof
areveryclosetoeachotherfor1≤
thatthechoiceoftheC-strategyρhas
Boundingthex=ncasecorresponds
onecolumns.InEquation(4)we
average.Weﬁnishtheproofbybounding
thechancethatnobodyisaccusedby
Accused
statingthatourﬁngerprintcodeaccuses
probability.
,andρbeasinthetheorem.Weassume
\[n\],n≤casthecodewordsoftheusers
bedistributedaccordingtothecodeFncǫ.
(p1, . . . , pm).Forsimplicityweintroduce
deﬁnitionUji= qiifXji= 1andUji= −1/qi
j=Pm
i=0yiUjiforj∈C.Let

<a id="ssp-us-prior-art-c3-para-00049"></a>
,
(1)
yi
xiqi −n −xi
qi
number of ones in column i of X.Recall that

<a id="ssp-us-prior-art-c3-blockquote-00050"></a>
> <a id="ssp-us-prior-art-c3-para-00051"></a>
> Z.ThusifS\>nZatleastonepirate
> boundtheprobability
> )) = ∅\] ≤P\[S≤nZ\].
> proofisasfollows.Ifthepirateswould
> ofallzerosthenwewouldhaveS=0
> accusenobody.Unfortunatelyforthe
> iofXconsistsofallonestheymust
> andthisdeﬁnitelyincreasesS.They
> i where column
> decreaseSifthecolumncontainsfewer
> andincreaseSifthecolumncontains
> knowthenumberxiofonesofthecolumn
> thedistributionofpisuchthatthewins
> theirchoiceforyihasalmostnoeﬀecton
> ontheexponentialaverageE\[e−αS\]fora
> allone columns isthusimpossible to
> withveryhighprobability.
> partoftheproofwestudytheexponential
> \] and in Equation (2) we ﬁnd the largest value it can take for any
> proof we study that formula closely.We
> whichMxinEquation(2)isthemaximum
> x≤n −1.Thisrepresentsestablishing
> onlyaminoreﬀectontheexpectation.
> tocalculatingtheeﬀectonSoftheall
> establishasimpleboundontheexponential
> theprobabilityofS≤nZ(andthus
> σ)usingtheMarkovinequality.

<a id="ssp-us-prior-art-c3-horizontalrule-00052"></a>

---

<a id="ssp-us-prior-art-c3-header-00053"></a>
### Page 12

<a id="ssp-us-prior-art-c3-para-00054"></a>
Usingtherulesofthesecondphase
"X

<a id="ssp-us-prior-art-c3-header-00055"></a>
# e−αS = E E p,X p X m " X Y

<a id="ssp-us-prior-art-c3-para-00056"></a>
E
e−αS
p
i
X
The expectation in this formula is for the choice of
Xasgeneratedintheﬁrstandsecond
The summation is for all n by m
iofXisdenotedbyxi.UsingEquation
"m

<a id="ssp-us-prior-art-c3-para-00057"></a>
X
Y
E
E
px
p,X\[e−αS\] =
p
i
i=1
X
Herexiandy=ρ(X)isdetermined
p.Noticethatfor ﬁxedX
minedby
thusthesetermsareindependent.We
m
h
X
Y
E
Epi
p
p,X\[e−αS\] =
i
i=1
X
Theexpectationontherighthandside
Tosimplifytheexpression weletp
p
callywitheachpi,letq=
(1 −p)/p

<a id="ssp-us-prior-art-c3-para-00058"></a>
E0,x= Ep
h
px(1 −
E1,x= Ep
Eachyiiseither0or1,furthermore
yi= 1bythemarkingcondition.Thus
X
E
p,X\[e−αS\] ≤
X
wheremax∗denotestheﬁrsttermE0
and themaximum of thetwo terms
notdependontheC-strategyρ,and
themarkingconditionwehaveequality
theproductonlydependsonxiand
wecanswitchthesummationandthe
expectationofe−αS.Itisstilltight
E
p,X\[e−αS\] ≤
ofthecodegenerationwehave
m
!\#
Y

<a id="ssp-us-prior-art-c3-para-00059"></a>
pxi
e−αS
i(1 −pi)n−xi
i=1

<a id="ssp-us-prior-art-c3-header-00060"></a>
# 

<a id="ssp-us-prior-art-c3-para-00061"></a>
pxi
.
i(1 −pi)n−xi
=1
p in the ﬁrst phase or for
p and
phasesofgeneratingFncǫasindicated.
0-1 matrices X.The number of ones in column
(1)wehave
)\#
.
(1 −pi)n−xie−αyi(xiqi−n−xi
i
qi
p
byX,whileqi=
(1 −pi)/piisdetertermiof theproduct dependssolely onpi,
have
)i
xi
.
(1 −pi)n−xie−αyi(xiqi−n−xi
qi
istakenfortherandomvariablepi.
bearandomvariabledistributedidentiandintroduce
,
px(1 −p)n−x
p)n−xe−α(xq−n−x
.
q)i
ifxi=0thenyi=0andifxi=nthen
wehave
m
Y
max∗(E0,xi, E1,xi),
i=1
,xiifxi= 0,thelasttermE1,xiifxi= n
otherwise.Noticethatthislast bound does
astheonlyassumptionony=ρ(X)is
forsomeC-strategyρ.Astermiof
thesummationisforall0-1matricesX
producttogetourﬁnalboundonthe
forsomeC-strategyρ.
n
!m
n

<a id="ssp-us-prior-art-c3-para-00062"></a>
X
Mx
,
(2)
x
x=0

<a id="ssp-us-prior-art-c3-horizontalrule-00063"></a>

---

<a id="ssp-us-prior-art-c3-header-00064"></a>
### Page 13

<a id="ssp-us-prior-art-c3-para-00065"></a>
where
M0= E0,0
Mx= max(E0,x, E1
We use eu≤1+u+u2that holds for
inE1,x.If−α(xq −(n −x)/q) \< 1.7

<a id="ssp-us-prior-art-c3-para-00066"></a>
)≤1 −α
e−α(xq−n−x
xq −
q
Wemake theboundwork forall qby
totherighthandside.Hereχx(p)is
p ≥1 −α2(n −x)2,whichisimplied
Weremarkthatinthepreliminary
√
t/c.Thismakes−α(xq−(n −x)/q
theproofsimplerbygettingridof
valueforαmakes thecomputation
weakererrorboundisstillmorethan
butwestrivehereforthestrongest
Wehave
≤
px(1 −p)n−xe−α(xq−n−x
q)
Takingexpectationsweget
E1,x≤E0,x −αF
where

<a id="ssp-us-prior-art-c3-para-00067"></a>
px(1 −
F1,x= Ep
"
px(1 −p)n
F2,x= Ep

<a id="ssp-us-prior-art-c3-para-00068"></a>
χx(p)(1
Rx= Ep
The term F1,xis the most important.
surethatitissmallfor1≤x≤n −
,
Mn= E1,n,
,x)for1 ≤x ≤n −1.
u \< 1.7 to bound the exponential term
wehave

<a id="ssp-us-prior-art-c3-para-00069"></a>
2

<a id="ssp-us-prior-art-c3-para-00070"></a>
n −x
.

- <a id="ssp-us-prior-art-c3-bulletlist-00071"></a> <a id="ssp-us-prior-art-c3-list-item-00072"></a> <a id="ssp-us-prior-art-c3-plain-00073"></a> α2
    xq −n −x
    q
    q
    1−p
    addingtheextra termχx(p)eα(n−x)/√
    thecharacteristicfunctionoftheevent
    by−α(xq −(n −x)/q) \> 1.
    version\[15\]ofthispaperwechoseα=
    )\<1alwayshold,thuswecouldmake
    thetermχx(p).Unfortunately,thissmall
    yieldasomewhat weaker error bound.This
    enoughtoimplyCorollary3forhighc,
    boundsachievablebythesemethods.
    px(1 −p)n−x−

<a id="ssp-us-prior-art-c3-para-00074"></a>
xq −n −x
αpx(1 −p)n−x
+
q
2

<a id="ssp-us-prior-art-c3-para-00075"></a>
xq −n −x
+
α2px(1 −p)n−x
q
α(n−x)
√
χx(p)(1 −p)n−xe
1−p.
1,x + α2F2,x + Rx,

<a id="ssp-us-prior-art-c3-para-00076"></a>
p)n−x
xq −n −x
,
q
2\#

<a id="ssp-us-prior-art-c3-para-00077"></a>
−x
≥0,
xq −n −x
q
α(n−x)

<a id="ssp-us-prior-art-c3-para-00078"></a>
√
−p)n−xe
≥0.
1−p
Our choice of the distribution for p makes
1.Thespeciﬁcchoiceofthedistribution

<a id="ssp-us-prior-art-c3-horizontalrule-00079"></a>

---

<a id="ssp-us-prior-art-c3-header-00080"></a>
### Page 14

<a id="ssp-us-prior-art-c3-para-00081"></a>
isusedforthisboundonly.
Recall
r∈\[t′, π/2 −t′\],wheresin2t′= t.We
Zπ/2−t′
F1,x=
sin2xr
π/2 −2t′
t′
Notice that the primitive function of the integrand is
thuswehave
F1,x=f(π/2 −t′) −f(t′)
π/2 −2t′
Forthiscalculationthechoicet=
F1,x=0for1≤x≤n −1.Weneed
andalsointheproofofTheorem1.
yieldingasmallbutnonzerovaluefor
F1,x≥−tx
andget
Mx= max(E0,x, E1,x) ≤E0,x
WealsohaveM0= E0,0andsinceF1
Mn= E1,n≤E0,n −α(1
Nextweestimatethesummation
n
n
n
n

<a id="ssp-us-prior-art-c3-para-00082"></a>
X
X
≤
Mx
x
x
x=0
x=0
α(1 −t
n

<a id="ssp-us-prior-art-c3-para-00083"></a>
X
α2
x=0
Weboundeachtermseparately:
n
n
n

<a id="ssp-us-prior-art-c3-header-00084"></a>
# X X E0,x

<a id="ssp-us-prior-art-c3-header-00085"></a>
# x x=0 x=0

<a id="ssp-us-prior-art-c3-header-00086"></a>
# Ep

<a id="ssp-us-prior-art-c3-para-00087"></a>
Ep
thatp=sin2rwithauniformrandom
have1 −p = cos2r,q= cot rand
cos2n−2xr(x cot r −(n −x) tan r)dr.
f(r) = 1/2 sin2xr cos2n−2xr,
=tn−x(1 −t)x −tx(1 −t)n−x
.
π −4t′
0(nocutoﬀ)wouldbeoptimalyielding
t\>0inothercalculationsofthisproof
Thechoicet=1/(300c)isacompromise
F1,x.For1 ≤x ≤n −1weuse
(1 −t)n−x
\< 0
π −4t′

- <a id="ssp-us-prior-art-c3-bulletlist-00088"></a> <a id="ssp-us-prior-art-c3-list-item-00089"></a> <a id="ssp-us-prior-art-c3-plain-00090"></a> αtx(1 −t)n−x
- <a id="ssp-us-prior-art-c3-list-item-00091"></a> <a id="ssp-us-prior-art-c3-plain-00092"></a> α2F2,x + Rx.
    π −4t′
    ,n=(1−t)n−tn
    π−4t′
    −t)n −tn
- <a id="ssp-us-prior-art-c3-list-item-00093"></a> <a id="ssp-us-prior-art-c3-plain-00094"></a> α2F2,n + Rn.
    π −4t′
    inEquation(2)

<a id="ssp-us-prior-art-c3-para-00095"></a>
E0,x −
n

<a id="ssp-us-prior-art-c3-para-00096"></a>
)n −Pn
tx(1 −t)n−x
x=1
x
+
π −4t′
n
n

<a id="ssp-us-prior-art-c3-para-00097"></a>
n
X
Rx.
(3)
F2,x +
x
x
x=0
n

<a id="ssp-us-prior-art-c3-para-00098"></a>
Ep
px(1 −p)n−x
x
"n

<a id="ssp-us-prior-art-c3-header-00099"></a>
# 

<a id="ssp-us-prior-art-c3-para-00100"></a>
n

<a id="ssp-us-prior-art-c3-para-00101"></a>
X
px(1 −p)n−x
x
x=0
\[1\] = 1;

<a id="ssp-us-prior-art-c3-horizontalrule-00102"></a>

---

<a id="ssp-us-prior-art-c3-header-00103"></a>
### Page 15

<a id="ssp-us-prior-art-c3-para-00104"></a>
n
n

<a id="ssp-us-prior-art-c3-para-00105"></a>
X
tx(1 −t)
(1 −t)n−
x
x=1
n
n
n

<a id="ssp-us-prior-art-c3-para-00106"></a>
n

<a id="ssp-us-prior-art-c3-header-00107"></a>
# X X E F2,x

<a id="ssp-us-prior-art-c3-para-00108"></a>
x
x
x=0
x=0
"n

<a id="ssp-us-prior-art-c3-header-00109"></a>
# X

<a id="ssp-us-prior-art-c3-para-00110"></a>
Ep
x=0
Tofurthersimplifythisexpression
theindependentidenticallydistributed
P\[Uj= q\] = p and P\[Uj= −1/q\] = 1
variables have expectation 0 and variance 1, so we have
expectationisforaﬁxedpwithrespect
spellingoutthisexpectationyields
forpinthelastdisplayedequation.
n
n

<a id="ssp-us-prior-art-c3-para-00111"></a>
X
F2
x
x=0
Forthelasterrorterm

<a id="ssp-us-prior-art-c3-para-00112"></a>
χx(p
Rx= Ep
√
t/α
we have Rx= 0 for x \> n−
call that choosing α
Forany 0 ≤x ≤nthefunction(1 −p
√
t/αthe
in\[t, 1 −t\],soforx ≤n −
forp ∈\[t, 1 −t\]isatp = 1 −α2(n −x
Rx≤e(α(
n

<a id="ssp-us-prior-art-c3-para-00113"></a>
≤(ne
Using
x
n−x)n−xandnα ≤cα
√
t/α⌋
⌊n−
n
n

<a id="ssp-us-prior-art-c3-header-00114"></a>
# X X ≤ Rx x x=0 x=0 √ ⌊n− t/α X

<a id="ssp-us-prior-art-c3-para-00115"></a>
e
x=0
√
⌊n−
t/α
X
\<
e
x=0
√
\<
3 · 19−⌈
n−x= 2(1 −t)n−1 ≥1 −2nt;
"

<a id="ssp-us-prior-art-c3-para-00116"></a>
2\#
px(1 −p)n−x
xq −n −x
p
q

<a id="ssp-us-prior-art-c3-para-00117"></a>
2\#
n
px(1 −p)n−x
xq −n −x
x
q
let0\<p\<1beﬁxedandconsider
randomvariablesUjforj∈\[n\]with
p
−p, where q=
(1 −p)/p.These random
E\[(Pn
j=1Uj)2\] = n.This
totherandomvariablesUj.Formally
exactlytheformulainsidetheexpectation
Thisimplies
,x= Ep\[n\] = n.

<a id="ssp-us-prior-art-c3-para-00118"></a>
√
αn−x
)(1 −p)n−xe
1−p
as in this case χx(p) = 0 for p ∈\[t, 1−t\].(Resomewhat smaller we can get rid of this error term entirely.)
1−pismonotonedecreasing
)n−xeα(n−x)/√
1−p
maximumofχx(p)(1 −p)n−xeα(n−x)/√
)2.Thuswehave
n −x))2(n−x).
= 1/20weget
ne
n−x
e(α(n −x))2(n−x)
n −x
⌋
(e3n(n −x)α2)n−x
⌋
19−(n−x)
t/α⌉.

<a id="ssp-us-prior-art-c3-horizontalrule-00119"></a>

---

<a id="ssp-us-prior-art-c3-header-00120"></a>
### Page 16

<a id="ssp-us-prior-art-c3-para-00121"></a>
Nowwecanestimateeachtermin
n
n

<a id="ssp-us-prior-art-c3-para-00122"></a>
X
Mx\< 1 −α1 −2nt
x
π −4t′
x=0
Weusedn≤c,α=1/(20c)andt
inequalityaboveworksforc≥7only.
computeRxexactlytoprovethe
ByEquation(2)wehave
E
p,X\[e−αS\] \< (1
BytheMarkovinequalityandm = 100
P\[S≤nZ\] ≤P\[S≤cZ\] ≤
Asmentionedin thebeginningofthis
empty,sotheaboveboundprovesthe
TheUnreadableDigit
BoundonCode
Inthissectionwegivethedeﬁnition
printing,whichwehavealready
ittothestandard(arbitrarydigit)
boundonthecodelengthinthis
thestandardmodel(Theorem4)
codesthetwomodelsaretrivially
Deﬁnition5.1.Aunreadabledigit
overthe alphabetΣisa distribution
matrix overΣand σisan algorithm
copy)asinput,andproducesasubset
accusedusers).HereΣ′= Σ ∪\{?\},
For∅̸ = C⊆\[n\]anunreadable digit C
submatrixofXformedbytherows
stringy=ρ(X)∈Σ′masoutputand
conditions.Forallpositions1≤i≤
digitsXjiwithj∈C.Furthermore,
agreethenyi̸=?.Wesaythatan
against coalitions of sizecifforanyC
digitC-strategyρtheerrorprobability
P\[σ(ρ(X)) = ∅
isatmostǫ.
Equation(3):
√
t/α⌉\< 1 −α/4.

- <a id="ssp-us-prior-art-c3-bulletlist-00123"></a> <a id="ssp-us-prior-art-c3-list-item-00124"></a> <a id="ssp-us-prior-art-c3-plain-00125"></a> α2n + 3 · 19−⌈
    =1/(300c)here.Tobehonestthelast
    Forsmallervaluesofconeneedsto
    estimate.
    −α/4)m\< e−αm/4.
    (4)
    c2k,Z= 20ckweget
    e−αm/4
    e−αcZ= e−α(m/4−cZ)≤ǫc/4.
    proof,ifS\> nZthenC ∩σ(ρ(X))isnot
    theorem.
    ModelandtheLower
    Length
    oftheunreadabledigitmodelofﬁngermentionedinSections1and2.Wecompare
    modelinLemma5.3.Weproveourlower
    model,seeTheorem5.Thelowerboundin
    followsasacorollary.Notethatforbinary
    equivalent.
    ﬁngerprintcodeoflengthmfornusers
    overthe pairs(X, σ),whereXisan nby m
    thattakesa string y∈Σ′m(the illegitimate
    σ(y)⊆\[n\]:=\{1, 2, . . ., n\}(thesetof
    where?/∈Σrepresentstheunreadabledigit.
    -strategyisanalgorithmρthattakesthe
    withindicesinCasinput,andproducesa
    satisﬁesthefollowing(strongmarking)
    mthedigityiiseither?oroneofthe
    ifforsomeiallthevaluesXjiforj∈C
    unreadabledigitﬁngerprintcodeisǫ-secure
    ⊆\[n\]ofsize\|C\| ≤candanyunreadable
    orσ(ρ(X))̸ ⊆C\]

<a id="ssp-us-prior-art-c3-horizontalrule-00126"></a>

---

<a id="ssp-us-prior-art-c3-header-00127"></a>
### Page 17

<a id="ssp-us-prior-art-c3-para-00128"></a>
Atﬁrsttheunreadabledigitmodel
thearbitrarydigitmodel.Itintroduces
digits)forthepiratesandsimultaneously
todigitsinΣ.Acloserlookwilltell
unreadabledigitwithanyﬁxeddigit
becaught.Thissimpleobservationis
somedeﬁnitions.
Deﬁnition5.2.LetΣbeaﬁnite
?/∈Σandleta∈Σbearbitrary.
fa: Σ′∗→Σ∗thatreplaceseach
unchanged.LetFbean(arbitrary
ByFawedenotetheunreadabledigit
isdistributedaccordingtoF.
Lemma5.3.Ifan(arbitrarydigit)
ǫ-secureagainstanycoalitionofsize
Fa(fora ∈Σ)isalsoǫ-secureagainst
anarbitrarycoalitionandjisan
max
P\[j∈σ(ρ(X))\]
ρ
max
P\[C ∩σ(ρ(X)) = ∅\]
ρ
where the maxima are taken over C
ρ′,whiletheprobabilitiesareaccording
on(X, σ′).
Proof:Allthecomplicatedlooking
simpleobservation,thatforanunreadable
fa ◦ρ′isan(arbitrarydigit)C-strategy
σ′= σ ◦fa.
Lemma5.3tellsusthatthearbitrary
paper) demands moreof a ﬁngerprint code
particular,theﬁngerprintcodeFncǫ
digitﬁngerprintcode(Fncǫ)0(wesimply
thiscodesatisﬁesalltheniceproperties
3.
AlsobyLemma5.3thearbitrary
areequivalentoverabinaryalphabet.
equivalencedoesnotholdbutLemma
alphabetsandconcludedthatfora
abinaryalphabetisjustaspowerful
resultsofthispaper(Theorems1,2,
generality:forreasonable error parameters the
withinaconstant factorforbothmodels
ofarbitrarysizeatleasttwo.
mayappeartobeincomparablewith
anewpossibility(creatingunreadable
restrictstheirchoiceswithrespects
however,thatthepiratescanreplaceany
a∈Σwithoutincreasingtheirchanceto
formalizedinLemma5.3.Westartwith
alphabetandletΣ′=Σ∪\{?\}forsome
Letusdenotebyfathetransformation
occurrenceof?byaandleavesallotherdigits
digit)ﬁngerprintcodeoverthealphabetΣ.
ﬁngerprintcode(X, σ ◦fa)where(X, σ)
ﬁngerprintcodeFoverthealphabetΣis
cthentheunreadablebitﬁngerprintcode
anycoalitionofsizec.Moreover,ifCis
arbitraryuserthenwehave
≥max
P\[j∈σ′(ρ′(X))\],
ρ′
≥max
P\[C ∩σ′(ρ′(X)) = ∅\],
ρ′
-strategies ρ, and unreadable digit C-strategies
tothedistributionsFon(X, σ)andFa
statementsofthelemmafollowfromthe
digitC-strategyρ′thefunctionρ =
andσ(ρ(X)) = σ′(ρ′(X))foranyXif
digitmodel(studiedinmostofthis
than theunreadable digit model.In
canbetriviallyextendedtoaunreadable
treatunreadabledigitsaszeros),and
statedinTheorems1,2andCorollary
digitandtheunreadabledigitmodels
Overlargeralphabetssuchadirect
5.3tellsuswhichmodelisstronger.
Lindkvist \[10\] studied the relative power of ﬁngerprinting over binary and larger
severelylimitedclassofﬁngerprintcodes
asarbitraryalphabetsare.
Themain
5)answerboththesequestionsinfull
optimalcodelengthisthesame
ofﬁngerprinting andover an alphabet

<a id="ssp-us-prior-art-c3-horizontalrule-00129"></a>

---

<a id="ssp-us-prior-art-c3-header-00130"></a>
### Page 18

<a id="ssp-us-prior-art-c3-para-00131"></a>
TomakeourlowerboundinTheorem
theunreadabledigitmodel.ByLemma
Theorem5.LetFbeanunreadable
anarbitraryalphabetΣfornusers.
1/(100ca)areal,wherea \> 1isa
(ii)below,then
m ≥da
whereda\> 0dependssolelyona.
(i) For any coalitionC⊂\[n\] of size \|
ρ,andanyuserℓ∈\[n\] \\ C
P\[ℓ∈
(ii)ForanycoalitionC⊆\[n\]of
strategyρ
P\[C ∩σ(
IndependentofourpaperPeikert,
icallyalmostidenticallowerbound
Theirresultonlyappliestoalimited
thenumberofcolumntypes:the
Xproducedbythecode.Inthecode
numberof columntypeswasseverely limited.
matriceswithallthecolumnsdiﬀerent.
applicable.Nevertheless,someofthe
\[11\]andinthispaperaresimilarand
Astheproofusesanesoteric
divergence)wemotivatethechoice
Assumewehaveaﬁngerprintcode
ofTheorem5.Weconcentrateonthe
thepiratecoalitionCℓ=\[c\] \\ \{ℓ\}
OurgoalistogivearandomizedCℓ
outputρℓ(X)ofthisstrategyisalmost
ofXandσasbeingﬁxed,andthe
strategy ρℓ.(Thissimpliﬁcation is
formalproof.Instead,weensurethe
areclosetoeachother.)
Therandomizedstrategiesρℓwe
randomizedstrategiesbiasstrategies.
independently for each digit yiof y=
they see on position i.The probability of
basedonhowmanyofthepiratesin
ThebiasfunctionmustgiveP\[yi=
positionitosatisfythemarking
4workinbothmodelswestateitin
5.3Theorem4follows.
digitﬁngerprintcodeoflengthmover
Let3≤c≤nbeanintegerand0\<ǫ\<
constant.IfFsatisﬁestheconditions(i)and
c2log(1/ǫ),
C\| = c−1, any unreadable digit C-strategy
σ(ρ(X))\] ≤ǫ.
size\|C\|=candanyunreadabledigitC-
ρ(X)) = ∅\] \< 0.99
Shelat,andSmithin\[11\]proveanumerforthelengthofbinaryﬁngerprintcodes.
classofcodeswithastrongboundon
numberofnon-equalcolumnsofthematrix
constructedbyBonehandShaw\[3\]the
Ourconstruction typicallyyields
Forsuchcodestheboundin\[11\]isnot
techniquesofthelowerboundproofsin
weshallcommentonthesesimilarities.
measureofdistancefordistributions(R´enyi
here.
(X, σ)satisfyingconditions(i)and(ii)
set\[c\]oftheﬁrstcusersonly.Consider
containingalltheseusersbutuserℓ∈\[c\].
-strategyρℓtothiscoalitionsuchthatthe
thesameforallℓ∈\[c\].Herewethink
randomization comingfromtherandomized
not fullyjustiﬁed and willnot beused in the
distributionsofthetriples(X, σ, ρℓ(X))
useareverysimple.Wecallthistypeof
InabiasC-strategyρthepiratesdecide
ρ(X) if it is ? or the most popular digit si
yi= si is determined by a bias function
Cseesiatpositioniintheircodewords.
si\]=1ifalloftheircodewordsagreeat
condition,whileifthemostpopulardigitis

<a id="ssp-us-prior-art-c3-horizontalrule-00132"></a>

---

<a id="ssp-us-prior-art-c3-header-00133"></a>
### Page 19

<a id="ssp-us-prior-art-c3-para-00134"></a>
notseeninthemajorityoftherows
thecasewhenthemostpopulardigit
Letusﬁrstseewhathappensif
possibletoachieve.Whatistheaccused
tocondition(i)thissetdoesnot
morethanǫ,butaccordingto(ii)it
least 1/100.The contradiction is clear as
distributionsareimpossibletoachieve
Cℓ′mayseeadiﬀerentnumberofthe
Fortunately,thisdiﬀerenceisbounded
ofdistancebetweenthesedistributions.
usethesamepiratecoalitions,similar
bias function is similar to ours.
called idealwords) andtheyprovethat
willhitthistargetdistribution.
decreaseswiththenumberofcolumn
toomanycolumntypes.
Thesimplestmeasuretoconsider
isthemaximaldiﬀerenceinthe
distributions.
thediﬀerenceof1inthenumberof
causeadiﬀerence1/cintheprobability
single digit may diﬀer by as much as 1
ρℓ(X)andρℓ′(X)isatmostthesum
each digit is independent (recall, that we consider
ofpositionsm=o(c)theresulting
Butform \> cthisapproach gives
Abetterchoiceforthedistance
gence.
distribution(obtainedbythecoalition
egy).Withthecorrectchoiceofthe
individualdigitcontributesonlyO(1
canbebestunderstoodthroughthe
biasedcoin:itgivesheadswithprobability
coinisindistance1/cfromthefair
torealizethebias.)Thesedivergences
Unfortunately,theproperties(i)and (ii)
divergenceforthetotaldistributions
O(log(1/ǫ)/c).Wearethusbackata
Thecorrectchoiceofthedistance
vergence.Thisesotericversionof
Alfr´ed R´enyi in\[12\].Ithasseldombeen
R´enyidivergencefromacommontarget
thecoalition of all cplayers bya
wehaveP\[yi=?\] = 1toaccommodatefor
isnotunique.
identicallydistributedoutputsρℓ(X)were
setσ(ρℓ(X))inthiscase?According
containanyoftheplayerswithprobability
containsoneofthemwithprobabilityat
ǫ \< 1/(100c).Unfortunately, identical
asforℓ̸ =ℓ′thepiratecoalitionCℓand
mostpopulardigitatanygiven position.
by1.Thus,wehavetostudysomekind
The proof technique of \[11\] is almost identical to ours up to this point.They
verysimplestrategiesandeventheir
Their solution to the non-identical distributions
obtained is to designate a target distribution (the uniform distribution on the so
withsomesmallprobabilitytheoutput
However,thissmallprobabilityexponentially
types,anditbecomesuselessifthereare
istheusualdistanceindistribution.This
probabilitiesofanyeventaccordingtothetwo
It is easy to verify, that no matter how we choose the bias function
appearancesofthemostpopulardigitmay
P\[yi=?\].Thus,thedistributionofa
/c.The distance of the total distributions
ofthesedistancesasineachpiratedcopy
Xﬁxed).Thus, if the number
totaldistributionsareclosetoeachother.
nothing.
measureistheinformationtheoreticdiverFor technical reasons we must consider divergence from a common target
ofallcplayersbyasimilarbiasstratbiasfunctiononecanguaranteethatany
/c2)tothedivergence.(Thisphenomenon
followingexample:Supposeyouhavea
1/2 + 1/c.Thedistributionofyour
distributionbutyouneedΘ(c2)coinﬂips
addupfortheindependentpositions.
ofTheorem 5donotguarantee ahigh
ρℓ(X),thesedivergencescanbeaslowas
linearbound.
measureisthehigherorderR´enyidiinformationaldivergencewasintroducedby
used since.Again,wehavetomeasure
distributionρ(X)thatisobtainedby
similar bias\[c\]-strategy.R´enyi divergence still

<a id="ssp-us-prior-art-c3-horizontalrule-00135"></a>

---

<a id="ssp-us-prior-art-c3-header-00136"></a>
### Page 20

<a id="ssp-us-prior-art-c3-para-00137"></a>
hasthepropertythateachdigit
simplyaddupfortheindependent
parameters conditions (i) and (ii) of Theorem 5
Ω(log(1/ǫ)) between ρ(X) and ρℓ(X
calculationintheproofofTheorem5.
Deﬁnition5.4.R´enyidivergenceof
randomvariablesQandRisdeﬁned
Hα+1(Q\|\|R) =1
αlog
wherethesummationextendsoverthe
withpositiveprobability.Thedivergence
alsotakenwithpositiveprobabilityby
Noticethatthesedivergencesdepend
thevariablesQandRandnotontheir
propertiesofR´enyidivergencesare
lineproofs.
(a)IfQ1andQ2areindependentand
Hα+1((
= Hα+1(Q1\|\|
(b)
eαHα+1((Q,S)\|\|(R,S))=
wheretheexpectationistaken
(c)Foranyfunctionf
Hα+1(f(Q)\|\|
(d) If the random variables Q and R
P\[R = 1\] = s,0 \< s \< 1,then
Hα+1(Q\|\|R
Furthermore,ifq/s \< 10,(1 −q
Hα+1(Q\|\|
wheretheconstanthiddeninthe
contributesO(1/c2),andthesecontributions
digits.Butwiththecorrectchoiceofthe
now implyatotal divergence of
) for at least one value of ℓ.See the detailed
orderα + 1(α\>0)betweenthediscrete
as
X
!
(P\[Q = x\])α+1
,
(P\[R = x\])α
x
valuesxtakenbytherandomvariableQ
isonlydeﬁnedifallthesevaluesare
therandomvariableR.
onlyontheseparatedistributionsof
jointdistribution.Thefollowingbasic
wellknownandhavestraightforwardone
R1andR2areindependent,then
Q1, Q2)\|\|(R1, R2))
R1) + Hα+1(Q2\|\|R2).
E\[eαHα+1((Q\|S=s0)\|\|(R\|S=s0))\],
forthevalues0oftherandomvariableS.
f(R)) ≤Hα+1(Q\|\|R).
take values from \{0, 1\} and P\[Q = 1\] = q,
qα+1

<a id="ssp-us-prior-art-c3-para-00138"></a>
.
) ≥1
αlog
sα
)/(1 −s) \< 10,then

<a id="ssp-us-prior-art-c3-para-00139"></a>
(q −s)2
,
R) = O
s(1 −s)
Onotationdependsonlyonα.

<a id="ssp-us-prior-art-c3-horizontalrule-00140"></a>

---

<a id="ssp-us-prior-art-c3-header-00141"></a>
### Page 21

<a id="ssp-us-prior-art-c3-para-00142"></a>
Usingthepropertiesabovewe
aboveformal.
ProofofTheorem5:Westartby
unreadable digit bias C-strategies the
ﬁrstcusersonly.Weapplycondition
probabilisticunreadabledigitCℓ-strategy
(ii) with the coalition C0= \[c
ρ0deﬁnedbelow.
Letusstartwiththec=3case,
aresimplerandsomewhatdiﬀerent
deterministicalgorithmproducingy
yi=s∈ΣifXji=sforatleasttwo
ifallthreevaluesXjiforj∈C0are
randomizedalgorithmproducingeach
Cℓ-strategywithequalprobability.In
outputy= ρℓ(X)areindependentand
j∈Cℓ,andifthevaluesXjiarediﬀerent
ofthethesetwovaluesor?with
Forthedeﬁnitionofthestrategies
Lettherealfunctionfbedeﬁned
0≤x≤1,andf(x)=1forx≥1.
propertythatcanbeeasilyveriﬁed.
(\*)Iftherealsuandvsatisfy0\<
f(u) ≤9f(v),1 −f(u) ≤9(1 −
(f(u) −f(
f(v)(1 −f
For0 ≤ℓ≤cand1≤i ≤mletk
amongthedigitsXjiwithj∈Cℓ,
multiplicity.
Wedeﬁnethebiasunreadabledigit
thefollowingrules.
ForﬁxedXand
independentlyfromyi∈\{sℓ
i, ?\}with

f

P\[yi= sℓ
i\] =
f

To check that ρℓisindeed an unreadable digit
markingcondition:ifkℓ
i= \|Cℓ\|then
positiveprobabilityonlyifsℓ
iisthe
j∈Cℓ,andinthiscasethereisno
Bycondition(ii)P\[C∩σ(ρ0(X))
accordingtothedistributionFon(
maketheproofoftheTheorem5outlined
describingthepiratecoalitionsCandthe
proof isbased on.Weconcentrate on the
(i)forℓ∈\[c\],Cℓ=\[c\] \\ \{ℓ\}andthe
ρℓdeﬁnedbelow.Weusecondition
\] and the probabilistic unreadable digit C0-strategy
heretheunreadabledigitCℓ-strategies
fromthec\>3case.Forρ0wetakethe
=ρ0(X),withithdigit(1≤i≤m)
ofthethreeindicesj∈C0andyi=?
distinct.Forρℓwithℓ∈\[c\]wetakethe
outputallowedforanunreadabledigit
otherwords,forℓ∈\[c\]thedigitsofthe
for1 ≤i ≤myi= sifXji= sforboth
forthetwoj∈Cℓ,thenyitakesone
probability1/3each.
ρℓforc \> 3weneedsomepreparations.
byf(x) = 0ifx ≤0,f(x) = 3x2−2x3if
Thisfunctionwaschosenforthefollowing
v\<1,u≤3vand1 −u≤3(1 −v)then
f(v))and
v))2

<a id="ssp-us-prior-art-c3-para-00143"></a>
.
(u −v)2
(v))= O
ℓ
ibethemaximummultiplicityofadigit
andletsℓ
ibeoneofthedigitswiththis
Cℓ-strategyρℓfor0≤ℓ≤c≥4with
ℓ,thedigitsofy=ρℓ(X)arechosen

<a id="ssp-us-prior-art-c3-para-00144"></a>
2kℓ
ifℓ\> 0
i−c+1
c−1
2k0

<a id="ssp-us-prior-art-c3-para-00145"></a>
ifℓ= 0.
i−c−1
c−3
Cℓ-strategy weneed tocheck the
yi= sℓ
i.Noticethatyi= sℓ
ihappenswith
absolutemajorityofthedigitsXjiwith
ambiguityinthedeﬁnitionofsℓ
i.
=∅\]\<0.99.
Heretheprobabilityis
X, σ)andaccordingtotherandomchoices

<a id="ssp-us-prior-art-c3-horizontalrule-00146"></a>

---

<a id="ssp-us-prior-art-c3-header-00147"></a>
### Page 22

<a id="ssp-us-prior-art-c3-para-00148"></a>
takeninρ0.Thusthereisauserj∈
more than 1/(100c).Assume
1andwehave
P\[1 ∈σ(ρ0
Wecontrastthiswiththeboundgiven
P\[1 ∈σ(
Ourgoalistoﬁnishtheproofby
enoughthenthedistributions(ρ0(X)
eachothertolettheseparationstated
Let α
ainthetheorem.
Letusﬁrstconsidertherandom
arbitraryﬁxedX.
Forc = 3itisstraightforward to
Hα+1(yi\|\|y′
i) =
Ourﬁrstgoalistoproveasimilar
Supposec \> 3.For1 ≤i ≤mwe
ifk0
i≥c/2 + 1inwhichcases0
iappears
digitsXjiforj∈C1,thuss0
iisan
Thus,bothyiandy′
itakevaluefrom
q= P\[yi= s1
i\] = f(q0
r= P\[y′
i= s1
i\] = f(r0
Herek0
i=k1
iork0
i=k1
i+ 1.Now
impliesq=1,inbothcasesHα+1(yi
alsohaveq0≤3r0and(1 −q0) ≤3(1
yieldsq≤10r,1 −q≤10(1 −r)and
(q −r)2
r(1 −r)=
Straitforwardcalculationsyieldthe
twoobservationsandproperty(d)of

<a id="ssp-us-prior-art-c3-para-00149"></a>
Hα+1(yi\|\|y′
i) = O
The hidden constant in the O
onlyonαandthusontheexponenta
\[c\]accusedbyσ(ρ0(X))withprobability
without loss of generality thatthisistrue foruser
(X))\] \>
(5)
100c.
bycondition(i):
ρ1(X))\] ≤ǫ.
(6)
showingthatifthecodeFisnotlong
, X, σ)and(ρ1(X), X, σ)aretoocloseto
inInequalities(5)and(6)happen.
be a positive parameter to be set later depending solely on the constant
variablesy= ρ0(X)andy′= ρ1(X)foran
see,that
O(1) = O(1/c2).
boundforc \> 3.
haveyi∈\{s0
i, ?\}andP\[yi= s0
i\] \> 0only
atleastk0
i−1 ≥c/2timesamongthe
absolutemajorityheretoo,ands1
i=s0
i.
\{s1
i, ?\}andbythedeﬁnition
i−c −1
,
)withq0=2k0
c −3
i−c + 1
)withr0=2k1
.
c −1
r=0impliesq=0andsimilarlyr=1
\|\|y′
i)=0.Ifwehave0\<r\<1thenwe
−r0),thusproperty(\*)ofthefunctionf
O((q0 −r0)2).
bound\|q0−r0\|=O(1/c).Usingthelast
theR´enyidivergenceweget

<a id="ssp-us-prior-art-c3-para-00150"></a>
1

<a id="ssp-us-prior-art-c3-para-00151"></a>
(q −r)2
= O
.
r(1 −r)
c2
notation here and elsewhere in this section depends
inthetheorem.

<a id="ssp-us-prior-art-c3-horizontalrule-00152"></a>

---

<a id="ssp-us-prior-art-c3-header-00153"></a>
### Page 23

<a id="ssp-us-prior-art-c3-para-00154"></a>
Nextweapplyproperty(a)ofthe
consider Xto beﬁxed,and thus all the
Sowehave
Hα+1(y\|\|y
Ournextgoalistoconsider(X, σ
prove

<a id="ssp-us-prior-art-c3-para-00155"></a>
Hα+1
(ρ0(X), X, σ)\|\|(
Indeed,byproperty(b)oftheR´enyi
exponentialaverageofthecorresponding
Equation (7)boundsallthosedivergences,
andEquation(8)isveriﬁed.
Nowweapplyproperty(c)ofthe
g(y, X, σ) = χ1∈σ
thattellsifuser1isaccused.From
Hα+1(χ1∈σ(ρ0(X))\|\|χ1∈σ(ρ1(X))) ≤Hα
Inequalities(5) and(6) andproperty (d)
lefthandsideisatleast

<a id="ssp-us-prior-art-c3-para-00156"></a>
αlog
(100c)α+1ǫ
Thelastboundcan bemadetrueby
exponentintheǫ \< 1/(100ca)condition
Puttingthelasttwodisplayed
m = Ω(
withtheconstantintheΩnotation
ConcludingRemarks
1.GuthandPﬁtzmannin\[7\]introduce
Theyassumethefollowingrelaxed
positionwherethecodewordofall
abilityofbeingabletooutputa
forallthepositionsofagreementand
arenotrestrictedatallinthedigit
wheretheuserscannotdetectthe
ﬁngerprint is embedded but they are allowed to modify a
document,thusalsomodifyingsome
R´enyidivergence.Recallthatwestill
digits of both yand y′are independent.
m

<a id="ssp-us-prior-art-c3-para-00157"></a>
′) = O
.
(7)
c2
)tobedistributedaccordingtoFand

<a id="ssp-us-prior-art-c3-para-00158"></a>
m

<a id="ssp-us-prior-art-c3-para-00159"></a>
.
(8)
ρ1(X), X, σ)
= O
c2
divergencetheabovedivergenceisan
divergenceswithﬁxed(X, σ).
As
theboundalsoholdsfortheirmean
R´enyidivergenceforthefunction
1if1 ∈σ(y)
(y)=
0if1/∈σ(y),
Equation(8)weget

<a id="ssp-us-prior-art-c3-para-00160"></a>
m
.
+1((ρ0(X), X, σ)\|\|(ρ1(X), X, σ)) = O
c2
of theR´enyi divergence showthatthe

<a id="ssp-us-prior-art-c3-para-00161"></a>
a −1
≥
α
2a + 10 log(1/ǫ).
settingα = 12/(a −1),wherea \> 1isthe
ofthetheorem.
equationstogetherweget
c2log(1/ǫ))
dependingonlyona,asrequired.
arelaxationofthemarkingcondition.
versionofthemarkingcondition:Atany
piratesagreethepiratesstillhaveaδprobdiﬀerentdigit.Thishappensindependently
iftheycanoutputadiﬀerentdigitthey
theyoutput.Thismodelsthesituations
positionsinadigitaldocumentwherethe
δfraction oftheentire
digitsoftheﬁngerprintcodewheresuch

<a id="ssp-us-prior-art-c3-horizontalrule-00162"></a>

---

<a id="ssp-us-prior-art-c3-header-00163"></a>
### Page 24

<a id="ssp-us-prior-art-c3-para-00164"></a>
modiﬁcation isagainst themarking condition.
digitalimages,audioorvideoﬁlesthis
Althoughthepiratesareless
cannotfoolourﬁngerprintcodesFncǫ
rem 1 does not use themarking condition,
TheproofofTheorem2however
Theproofisbasedonboundingthe
maintermintheboundcomesfrom
codewordscoincideandthemarking
revealsthatitisenoughthatthe
ofthesepositionsofagreementand
similar bound in therelaxed model
followingholds:
Theorem2’.ConsidertheFncǫcode
ofsize\|C\| ≤(1 −2δ)c,andletρbeany
andPﬁtzmann.Wehave
P\[C ∩σ(ρ(
wheretheprobabilityisaccordingto
codeFncǫ.
NoticethatforTheorem2’towork
considerthecodeFnc′ǫforc′=⌈c/
factorlongerthanFncǫforanyﬁxed
ﬁngerprintcodeifδ≥1/2evena
sequence,thusallﬁngerprintingis
2.
fromtheillegitimatecopycanbe
fractionoftheﬁngerprintcodeis
O(c)isǫ-secureagainstcoalitionsof
simplytreatallunknowndigitsas
3.Considerthehigh-errorcaseof
digit)ﬁngerprintcodesomebodyis
cwithatleastonepercentprobability
withmorethanǫprobability.
Using
thancTheorem4impliesthatthe
(thehiddenconstantdependsonb).
accusation algorithmoftheﬁngerprint
bylettingitaccuseeachuserindependently
thoseaccusedbytheoriginalalgorithm
aboverequirementswithlengthm =
4.Letusendthepaperwitha
cryptography.Itseemsthatﬁngerprinting
If theﬁngerprint is embeddedin
relaxationseemstobenatural.
restrictedintheiroutputinthiscase,they
muchbetter.Indeed,theproofofTheothusremains valid in thismodel too.
heavilydependsonthemarkingcondition.
expectationofarandomvariable,andthe
thecontributionofthepositionswhereall
conditionapplies.Acloserlookhowever
markingconditionappliesforalargefraction
thusexactlythesameargumentgivesa
of Guth and Pﬁtzmann.More precisely,the
andletδ\< 1/2,letC⊆\[n\]beacoalition
C-strategyintherelaxedmodelofGuth
X)) = ∅\] \< ǫc/4,
thedistributionon(X, σ)deﬁnedbythe
forcoalitionsofsizecweonlyhaveto
(1 −2δ)⌉,acodethatisonlyaconstant
δ\<1/2.Alsonoticethatforanybinary
singlepiratecanoutputauniformrandom
impossibleinthiscase.
The situation when only a fraction of the ﬁngerprint code can be retrieved
handledverysimilarly.Ifarandompositive
retrieved,thenthecodeFnc′ǫwithsomec′=
sizec.Toapplytheaccusationalgorithm,
zeros.
ǫ ≥1/c.Assumethatforan(unreadable
accusedfromallcoalitionsofsizeatmost
andnoﬁxedinnocentpersonisaccused
coalitionsofsizesubstantiallysmaller
codelengthisΩ(1/ǫb)forarbitraryb\<2
Itiseasytoseethatifwechangethe
codeFnc′ǫ′withc′= ⌊2/ǫ⌋andǫ′= ǫ/2
withprobabilityǫ/2inadditionto
wegetaﬁngerprintcodesatisfyingthe
O(log(1/ǫ)/ǫ2).
philosophicalremarkonﬁngerprintingand
isacryptographicprimitivewhose

<a id="ssp-us-prior-art-c3-horizontalrule-00165"></a>

---

<a id="ssp-us-prior-art-c3-header-00166"></a>
### Page 25

<a id="ssp-us-prior-art-c3-para-00167"></a>
mathematicalanalysisdoesnotdepend
putational complexity does not seem to play any role here.
thecomplexityassumptionexists,it
markingcondition(orevenitsrelaxation)
userscannotdetectthepositionsin
ishiddenunlesstheyseeadiﬀerence
casesthisassumptiontranslatesto
Acknowledgements
andJ´anosPachforalotofhelpin
References
\[1\]G.R.Blakley, C.Meadows and G.
messages, Proc. of Crypto ’85
180–189.
\[2\]D.BonehandM.Franklin,An
Proc. of Crypto ’99
\[3\]D.BonehandJ.Shaw,
IEEETransactionsofInformation
\[4\]B.Chor,A.FiatandM.Naor,
839,Springer-VerlagBerlin,
\[5\]F.Chung,R.Graham,T.Leighton,
ofCombinatorics8(1),2001.
\[6\]A.Fiat,T.Tassa,Dynamictraitor
(2001),211–223.
\[7\]J.GuthandB.Pﬁtzmann,Errordigitaldata,InformationHiding
Berlin2000,pp.134-145.
\[8\]J.Kilian,T.Leighton,L.
Resistanceofdigitalwatermarks
1998IEEEInternationalSymposium
\[9\]K.KurosawaandY.Desmedt,
schemes, Advances in cryptology—EUROCRYPT’98
Berlin,1998,pp.145–157.
\[10\]T.Lindkvist,Fingerprintingdigital
enceandTechnology,ThesisNo.
oncomplexityassumptions,andcomNotice however, that
ishiddeninthemarkingcondition.The
isbasedontheassumptionthatthe
adigitaldocumentwheretheﬁngerprint
intheircopiesofthedocument.Inmost
somekindofacomplexityassumption.
The author thanks Dezs˝o Mikl´os for introducing him to the area of ﬁngerprinting
writingthispaper.
B.Purdy,Fingerprinting longforgiving
Springer-Verlag Berlin, Heidelberg, 1985, pp.
eﬃcientpublickeytraitortracingscheme,
Springer-Verlag, Berlin, Heidelberg, 1999, pp. 338–353.
Collusion-secureﬁngerprintingfordigitaldata,
Theory44(1998),480–491.
Tracingtraitors,Proc.ofCrypto’94LNCS
Heidelberg,1994,pp.257–270.
Guessingsecrets,ElectronicJournal
tracing,JournalofCryptology14(3)
andcollusion-secureﬁngerprintingfor
(IH’99)LNCS1768,Springer-Verlag,
Matheson,T.Shamoon,R.Tarjan,F.Zane,
tocollusiveattacks,in:Proceedingsof
onInformationTheory,p.71.
Optimumtraitortracingandasymmetric
LNCS 1403, Springer,
documents,Link¨opingStudiesinSci798,1999.

<a id="ssp-us-prior-art-c3-horizontalrule-00168"></a>

---

<a id="ssp-us-prior-art-c3-header-00169"></a>
### Page 26

<a id="ssp-us-prior-art-c3-para-00170"></a>
\[11\]C.Peikert,A.Shelat,A.Smith,
printing,in:Proceedingsofthe
DiscreteAlgorithms(SODA)2003
\[12\]A.R´enyi,Probabilitytheory,
icsandMechanics,Vol.10.
London;AmericanElsevier
\[13\]R.Safavi-NainiandY.Wang,
Crypto’2000,LNCS1880,
316–332.
\[14\]J.N.Staddon,D.R.Stinson,R.
proof and traceability codes,
(2001),1042–1049.
\[15\]G.Tardos,Optimalprobabilistic
35thAnnualACMSymposium
125.
\[16\]T. Tassa, Low bandwidth dynamic traitor tracing schemes,
tology,toappear.
\[17\]Y.Yacobi,ImprovedBoneh-Shaw
cryptology—CT-RSA 2001
391.
\[18\]N. Wagner, Fingerprinting,
andPrivacy(1983),pp.18–22.
Lowerboundsforcollusion-secureﬁnger14thAnnualACM-SIAMSymposiumon
,pp.472–479.
North-HollandSeriesinAppliedMathematNorth-HollandPublishingCo.,Amsterdam,
PublishingCo.,Inc.,NewYork,1970.
Sequentialtraitortracing,in:
Proc.of
Springer-VerlagBerlin,Heidelberg,2000,pp.
Wei,CombinatorialpropertiesofframeIEEE Transactions of Information Theory 47
ﬁngerprintcodes,in:Proceedingsofthe
onTheoryofComputing,2003,pp.116–
Journal of Crypcontentﬁngerprinting,in:
Topicsin
, LNCS 2020, Springer-Verlag Berlin, 2001, 378–
Proc. of the 1983 IEEE Symposium on Security

<a id="ssp-review-metadata"></a>
## Structured-source metadata

| Field | Current value |
|---|---|
| Document ID | us-prior-art-c3 |
| Artifact family | prior-art-transcription |
| Jurisdiction | US |
| Scope | prior-art |
| Status | review-aid |
| Language | en |
| Title | C3 — Tardos, “Optimal Probabilistic Fingerprint Codes” — author-hosted extended version of the STOC 2003 paper |
| Authority scheme | PDF evidence transcription |

<a id="ssp-review-dependencies"></a>
## Dependencies

| Kind | Subject | Exact binding digest |
|---|---|---|
| None | — | — |

<a id="ssp-review-provenance"></a>
## Provenance

| Fragment | Stored source | Page | Region | Uncertainty |
|---|---|---:|---|---|
| [us-prior-art-c3-blockquote-00002](#ssp-us-prior-art-c3-blockquote-00002) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c3-blockquote-00040](#ssp-us-prior-art-c3-blockquote-00040) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-blockquote-00050](#ssp-us-prior-art-c3-blockquote-00050) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c3-bulletlist-00071](#ssp-us-prior-art-c3-bulletlist-00071) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-bulletlist-00088](#ssp-us-prior-art-c3-bulletlist-00088) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-bulletlist-00123](#ssp-us-prior-art-c3-bulletlist-00123) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00001](#ssp-us-prior-art-c3-header-00001) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c3-header-00007](#ssp-us-prior-art-c3-header-00007) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00010](#ssp-us-prior-art-c3-header-00010) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00013](#ssp-us-prior-art-c3-header-00013) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 3 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00016](#ssp-us-prior-art-c3-header-00016) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 4 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00019](#ssp-us-prior-art-c3-header-00019) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 5 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00022](#ssp-us-prior-art-c3-header-00022) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00025](#ssp-us-prior-art-c3-header-00025) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 7 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00028](#ssp-us-prior-art-c3-header-00028) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 8 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00031](#ssp-us-prior-art-c3-header-00031) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00034](#ssp-us-prior-art-c3-header-00034) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00037](#ssp-us-prior-art-c3-header-00037) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00047](#ssp-us-prior-art-c3-header-00047) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00053](#ssp-us-prior-art-c3-header-00053) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00055](#ssp-us-prior-art-c3-header-00055) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00060](#ssp-us-prior-art-c3-header-00060) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00064](#ssp-us-prior-art-c3-header-00064) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00080](#ssp-us-prior-art-c3-header-00080) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00084](#ssp-us-prior-art-c3-header-00084) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00085](#ssp-us-prior-art-c3-header-00085) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00086](#ssp-us-prior-art-c3-header-00086) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00099](#ssp-us-prior-art-c3-header-00099) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00103](#ssp-us-prior-art-c3-header-00103) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00107](#ssp-us-prior-art-c3-header-00107) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00109](#ssp-us-prior-art-c3-header-00109) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00114](#ssp-us-prior-art-c3-header-00114) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00120](#ssp-us-prior-art-c3-header-00120) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00127](#ssp-us-prior-art-c3-header-00127) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00130](#ssp-us-prior-art-c3-header-00130) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00133](#ssp-us-prior-art-c3-header-00133) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 19 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00136](#ssp-us-prior-art-c3-header-00136) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00141](#ssp-us-prior-art-c3-header-00141) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 21 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00147](#ssp-us-prior-art-c3-header-00147) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00153](#ssp-us-prior-art-c3-header-00153) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00163](#ssp-us-prior-art-c3-header-00163) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00166](#ssp-us-prior-art-c3-header-00166) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c3-header-00169](#ssp-us-prior-art-c3-header-00169) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00006](#ssp-us-prior-art-c3-horizontalrule-00006) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c3-horizontalrule-00009](#ssp-us-prior-art-c3-horizontalrule-00009) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00012](#ssp-us-prior-art-c3-horizontalrule-00012) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00015](#ssp-us-prior-art-c3-horizontalrule-00015) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 3 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00018](#ssp-us-prior-art-c3-horizontalrule-00018) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 4 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00021](#ssp-us-prior-art-c3-horizontalrule-00021) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 5 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00024](#ssp-us-prior-art-c3-horizontalrule-00024) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00027](#ssp-us-prior-art-c3-horizontalrule-00027) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 7 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00030](#ssp-us-prior-art-c3-horizontalrule-00030) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 8 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00033](#ssp-us-prior-art-c3-horizontalrule-00033) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00046](#ssp-us-prior-art-c3-horizontalrule-00046) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00052](#ssp-us-prior-art-c3-horizontalrule-00052) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00063](#ssp-us-prior-art-c3-horizontalrule-00063) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00079](#ssp-us-prior-art-c3-horizontalrule-00079) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00102](#ssp-us-prior-art-c3-horizontalrule-00102) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00119](#ssp-us-prior-art-c3-horizontalrule-00119) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00126](#ssp-us-prior-art-c3-horizontalrule-00126) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00129](#ssp-us-prior-art-c3-horizontalrule-00129) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00132](#ssp-us-prior-art-c3-horizontalrule-00132) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00135](#ssp-us-prior-art-c3-horizontalrule-00135) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 19 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00140](#ssp-us-prior-art-c3-horizontalrule-00140) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00146](#ssp-us-prior-art-c3-horizontalrule-00146) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 21 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00152](#ssp-us-prior-art-c3-horizontalrule-00152) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00162](#ssp-us-prior-art-c3-horizontalrule-00162) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00165](#ssp-us-prior-art-c3-horizontalrule-00165) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c3-horizontalrule-00168](#ssp-us-prior-art-c3-horizontalrule-00168) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c3-list-item-00072](#ssp-us-prior-art-c3-list-item-00072) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-list-item-00089](#ssp-us-prior-art-c3-list-item-00089) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-list-item-00091](#ssp-us-prior-art-c3-list-item-00091) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-list-item-00093](#ssp-us-prior-art-c3-list-item-00093) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-list-item-00124](#ssp-us-prior-art-c3-list-item-00124) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00003](#ssp-us-prior-art-c3-para-00003) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c3-para-00004](#ssp-us-prior-art-c3-para-00004) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c3-para-00005](#ssp-us-prior-art-c3-para-00005) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 1 | structured-transcription fragment | precise PDF page requires identified-human confirmation |
| [us-prior-art-c3-para-00008](#ssp-us-prior-art-c3-para-00008) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 1 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00011](#ssp-us-prior-art-c3-para-00011) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 2 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00014](#ssp-us-prior-art-c3-para-00014) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 3 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00017](#ssp-us-prior-art-c3-para-00017) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 4 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00020](#ssp-us-prior-art-c3-para-00020) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 5 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00023](#ssp-us-prior-art-c3-para-00023) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 6 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00026](#ssp-us-prior-art-c3-para-00026) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 7 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00029](#ssp-us-prior-art-c3-para-00029) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 8 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00032](#ssp-us-prior-art-c3-para-00032) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 9 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00035](#ssp-us-prior-art-c3-para-00035) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00036](#ssp-us-prior-art-c3-para-00036) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00038](#ssp-us-prior-art-c3-para-00038) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00039](#ssp-us-prior-art-c3-para-00039) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00041](#ssp-us-prior-art-c3-para-00041) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00042](#ssp-us-prior-art-c3-para-00042) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00043](#ssp-us-prior-art-c3-para-00043) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00044](#ssp-us-prior-art-c3-para-00044) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00045](#ssp-us-prior-art-c3-para-00045) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 10 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00048](#ssp-us-prior-art-c3-para-00048) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00049](#ssp-us-prior-art-c3-para-00049) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00051](#ssp-us-prior-art-c3-para-00051) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 11 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00054](#ssp-us-prior-art-c3-para-00054) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00056](#ssp-us-prior-art-c3-para-00056) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00057](#ssp-us-prior-art-c3-para-00057) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00058](#ssp-us-prior-art-c3-para-00058) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00059](#ssp-us-prior-art-c3-para-00059) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00061](#ssp-us-prior-art-c3-para-00061) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00062](#ssp-us-prior-art-c3-para-00062) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 12 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00065](#ssp-us-prior-art-c3-para-00065) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00066](#ssp-us-prior-art-c3-para-00066) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00067](#ssp-us-prior-art-c3-para-00067) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00068](#ssp-us-prior-art-c3-para-00068) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00069](#ssp-us-prior-art-c3-para-00069) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00070](#ssp-us-prior-art-c3-para-00070) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00074](#ssp-us-prior-art-c3-para-00074) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00075](#ssp-us-prior-art-c3-para-00075) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00076](#ssp-us-prior-art-c3-para-00076) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00077](#ssp-us-prior-art-c3-para-00077) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00078](#ssp-us-prior-art-c3-para-00078) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00081](#ssp-us-prior-art-c3-para-00081) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00082](#ssp-us-prior-art-c3-para-00082) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00083](#ssp-us-prior-art-c3-para-00083) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00087](#ssp-us-prior-art-c3-para-00087) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00095](#ssp-us-prior-art-c3-para-00095) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00096](#ssp-us-prior-art-c3-para-00096) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00097](#ssp-us-prior-art-c3-para-00097) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00098](#ssp-us-prior-art-c3-para-00098) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00100](#ssp-us-prior-art-c3-para-00100) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00101](#ssp-us-prior-art-c3-para-00101) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00104](#ssp-us-prior-art-c3-para-00104) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00105](#ssp-us-prior-art-c3-para-00105) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00106](#ssp-us-prior-art-c3-para-00106) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00108](#ssp-us-prior-art-c3-para-00108) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00110](#ssp-us-prior-art-c3-para-00110) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00111](#ssp-us-prior-art-c3-para-00111) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00112](#ssp-us-prior-art-c3-para-00112) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00113](#ssp-us-prior-art-c3-para-00113) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00115](#ssp-us-prior-art-c3-para-00115) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00116](#ssp-us-prior-art-c3-para-00116) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00117](#ssp-us-prior-art-c3-para-00117) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00118](#ssp-us-prior-art-c3-para-00118) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 15 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00121](#ssp-us-prior-art-c3-para-00121) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00122](#ssp-us-prior-art-c3-para-00122) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 16 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00128](#ssp-us-prior-art-c3-para-00128) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 17 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00131](#ssp-us-prior-art-c3-para-00131) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 18 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00134](#ssp-us-prior-art-c3-para-00134) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 19 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00137](#ssp-us-prior-art-c3-para-00137) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00138](#ssp-us-prior-art-c3-para-00138) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00139](#ssp-us-prior-art-c3-para-00139) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 20 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00142](#ssp-us-prior-art-c3-para-00142) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 21 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00143](#ssp-us-prior-art-c3-para-00143) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 21 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00144](#ssp-us-prior-art-c3-para-00144) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 21 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00145](#ssp-us-prior-art-c3-para-00145) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 21 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00148](#ssp-us-prior-art-c3-para-00148) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00149](#ssp-us-prior-art-c3-para-00149) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00150](#ssp-us-prior-art-c3-para-00150) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00151](#ssp-us-prior-art-c3-para-00151) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 22 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00154](#ssp-us-prior-art-c3-para-00154) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00155](#ssp-us-prior-art-c3-para-00155) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00156](#ssp-us-prior-art-c3-para-00156) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00157](#ssp-us-prior-art-c3-para-00157) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00158](#ssp-us-prior-art-c3-para-00158) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00159](#ssp-us-prior-art-c3-para-00159) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00160](#ssp-us-prior-art-c3-para-00160) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00161](#ssp-us-prior-art-c3-para-00161) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 23 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00164](#ssp-us-prior-art-c3-para-00164) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 24 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00167](#ssp-us-prior-art-c3-para-00167) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 25 | structured-transcription fragment | None declared |
| [us-prior-art-c3-para-00170](#ssp-us-prior-art-c3-para-00170) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 26 | structured-transcription fragment | None declared |
| [us-prior-art-c3-plain-00073](#ssp-us-prior-art-c3-plain-00073) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 13 | structured-transcription fragment | None declared |
| [us-prior-art-c3-plain-00090](#ssp-us-prior-art-c3-plain-00090) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-plain-00092](#ssp-us-prior-art-c3-plain-00092) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-plain-00094](#ssp-us-prior-art-c3-plain-00094) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 14 | structured-transcription fragment | None declared |
| [us-prior-art-c3-plain-00125](#ssp-us-prior-art-c3-plain-00125) | US/prior-art/C3/C3\_Tardos\_Optimal-probabilistic-fingerprint-codes.pdf | 16 | structured-transcription fragment | None declared |
