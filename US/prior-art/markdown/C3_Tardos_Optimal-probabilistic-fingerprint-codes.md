# C3 — Tardos, “Optimal Probabilistic Fingerprint Codes” — author-hosted extended version of the STOC 2003 paper

> **WORKING TRANSCRIPTION — NOT AN OFFICIAL COPY AND NOT FOR FILING.**
>
> Source: `../C3_Tardos_Optimal-probabilistic-fingerprint-codes.pdf` (see `../README.md` for that copy's provenance and verification status).
> Generated 20.07.2026. Extracted from the stored PDF's embedded text layer with PyMuPDF, using column-aware line placement (two-column pages are split at the gutter and each column emitted in reading order). No OCR.
>
> Text-layer extraction: characters are the publisher's own, not inferred. Reading order is reconstructed from line geometry, so paragraph flow across page and column breaks — and table alignment — still needs visual confirmation against the PDF. Line-number artifacts (5, 10, 15 …) may remain mid-sentence.

---

### Page 1

Optimal
G´abor
R´enyi
Pf.127,H-1354
Weconstructbinarycodesfor
codes for n users that are ǫ-secure against
Thisimprovesthecodesproposed
isapproximatelythesquareofthis
toworksusingtheBoneh-Shaw
traitortracingschemeofTassa[16].
Byprovingmatchinglower
codesisbestwithinaconstant
Thislowerboundgeneralizesthe
Shelat,and Smith [11] that applies to a limited class
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
tardos@renyi.hu
Abstract
ﬁngerprintingdigitaldocuments.Our
c pirates have length O(c2log(n/ǫ)).
byBonehandShaw[3]whoselength
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
inSTOC’03[15].Workonthispaperhas
Research&DevelopmentFund#2/019/2001,
OTKAT029255,OTKAT030059,andthegrant

---

### Page 2

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
andproducesasubsetσ(y) ⊆[n] := {
∅̸ = C⊆[n] a C-strategy is an algorithm
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
1, 2, . . ., n}(thesetofaccusedusers).For
ρ that takes the submatrix of Xformed

---

### Page 3

bytherowswithindicesinCasinput,
asoutput1andsatisﬁesthemarking condition
ifallthevaluesXjiforj∈Cagree
thataﬁngerprintcodeisǫ-secure against
ofsize|C| ≤candforanyC-strategy
P[σ(ρ(X)) = ∅
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
userisaccused,i.e.,that|σ(y)|=1.
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
coalitionsofsizec,ifforanyC⊆[n]
ρ,theerrorprobability
orσ(ρ(X))̸ ⊆C]
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

---

### Page 4

inthissubmatrix.
Thissubtle
ourconstructionissecureagainst
also,ourlowerboundworksinthis
based on very simplestrategies ρ
depends(in somerandomized manner) only
codewords(theithcolumnofthe
1.3
EarlierResults
Fingerprinting was ﬁrst studied by Wagner [18].
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
etal.[1].Manydiﬀerentmodelsfor
literature.SeeforexampleKilianetal.[8]for
thedocumentbutthedistanceshould
codeswereintroducedbyChoretal.[4].
pirateswhomustoutputapiratedcopy
ofthepiratedcopyisidenticaltotheith
haveaccessto.Thesecodesandthe
studied,seee.g.[2,9,13,14].Aswehave
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
Leighton[5]getaroundthisproblemby
“twooutofthesethreeplayersareguilty”
forlargercoalitions.Buteveninthe
beexponentialinthecoalitionsize.)
were introducedbyBoneh and Shaw[3].The
randomizationinarestrictedway.
They
matrixanduserandomizationonlyfor
thismatrix.We,ontheotherhand,use
byDeﬁnition1.1.BonehandShaw
m = O(n3log(n/ǫ))fornusersthatare
Againstcoalitionsofsizec<nthey

---

### Page 5

constructedǫ-secureﬁngerprintcodes
nusers.Infollow-upworksLindkvist
lengthnoteﬀectingtheasymptotics,
implementation of theBoneh-Shaw codes.
thenextsectionisapproximatelythe
Shawcodes.
Dynamictraitortracingwas
originallyadeterministicmodelrequiring
[16]introducedamoreeﬃcient
Shaw code as a primitive in his scheme.
nextsectionsubstantiallyimprovesthe
BonehandShawalsoproveanΩ(
ofﬁngerprintcodes.Ourlowerbound
matchestheconstructionifǫis
[11]prove alower boundfora
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
[10]mademinorimprovementonthe
whileYacobi[17]designedaveryeﬃcient
The length of our codes presented in
squarerootofthelengthoftheBonehintroducedbyFiatandTassa[6].Thiswas
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
theresultsin[11]alsopointtowardthe
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

---

### Page 6

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
valueri∈[t′, π/2 −t′]with0 < t′< π/
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
< ǫ < 1 and let k= ⌈log(1/ǫ)⌉.We deﬁne
lengthm=100c2kfornuserstobethe
X, σ).
phases.First,letpibeindependent,idenfrom[t, 1−t]forall1≤i≤m.
Here
bypickinguniformlyatrandomthe
4,sin2t′= t.
codematrixX,byselectingeachentry
{0, 1} with P[Xji= 1] = pi.Notice
holdsonlyin thesecond phase,theoverall
positivelycorrelatedasbothofthemtend
determinedbythevaluespiandthematrix
matrixUwithentries
−pi
ifXji= 1,
pi
pi
1−piifXji= 0.
copyy∈{0, 1}masinputif
Uji> Z,
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

---

### Page 7

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
boththeoremsn ≥c ≥1and0 < ǫ <
Theorem1.Let(X, σ)bedistributed
arbitraryuser,letC⊆[n] \ {j}bea
andletρbeanyC-strategy.Wehave
P[j∈σ
Theorem2.Let(X, σ)bedistributed
coalitionofsize|C| ≤c,andletρbe
P[C ∩σ(ρ(
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
accordingtoFncǫ.Letj∈[n]bean
coalitionofarbitrarysizenotcontainingj,
(ρ(X))] < ǫ.
accordingtoFncǫ.LetC⊆[n]bea
anyC-strategy.Wehave
X)) = ∅] < ǫc/4.
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

---

### Page 8

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
a > 1isaconstant.IfFsatisﬁes
m ≥da
whereda> 0dependssolelyona.
(i)ForanycoalitionC⊂[n]ofsize
anyuserj∈[n] \ C,wehave
P[j∈
(ii)ForanycoalitionC⊆[n]ofsize
have
P[C ∩σ(
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
integerand0 < ǫ < 1/(100ca)areal,where
conditions(i)and(ii)belowthen
c2log(1/ǫ),
|C| = c −1,foranyC-strategyρ,andfor
σ(ρ(X))] ≤ǫ.
|C|=c,andforanyC-strategyρ,we
ρ(X)) = ∅] < 0.99.
propertiesmuchstrongerthanrequiredfor
boundresult,Theorem 4,assumespropweakerthenthoserequiredforǫ-secure
This makes the matching lower and upper bounds even more interesting.
2,and4onecannoticethefollowing.

---

### Page 9

1.The length of our codes Fncǫ
codessatisfyingtheconditionsof
ByCorollary 3,thelengthofthecode
amongstallcodesfornusersthat
ǫ < 1/(100ca)foraﬁxeda > 1andǫ <
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
1 −νinplaceof0.99ifǫ < (ν/c)afor
wecanhaveacodeoflengthm=0:
probabilityatmostǫ.
are optimal within a constant factor amongst
Theorem4ifǫ < 1/(100ca)foraﬁxeda > 1.
Fncǫ
nisoptimalwithinaconstant factor
areǫ-secureagainstcoalitionsofsizecif
1/nbforaﬁxedb > 0.Theassumption
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
This answers the problem raised by Lindkvist [10] if binary
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
someconstanta > 1.Forn = c,ǫ = ν/c
simplyaccusearandomuser,eachwith

---

### Page 10

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
Wehaveﬁxedvaluespifrom[t, 1
choose Xjifrom {0, 1} independently
p
(1 −pi)/piifXji
Recallthatui=
FinallywesetS=Pm
i:yi
i=1yiui=P
S> Z,soweneedtoprovethatP[S
ConsidertheexpectedvalueE[eαS
rithm,andα = 1/(10c).Usingthe
have


= E
E
eαS
Y
i:yi=1
Next we use 1+u ≤eu≤1+u+u2
thesecondinequalityholdsforu<1
andthusαui< 1.Usingthatuihas
E [eαui] ≤E
= 1 + αE [ui] + α2
Y

E [eαui
=
E
eαS
i:yi=1
FinallybytheMarkovinequalitywe

P[S> Z] = P
eαS> e
Heretheexponentisα2m −αZ= −k
P[S> Z
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
−t]andaﬁxedstringy∈{0, 1}m.We
with P[Xji= 1] = piand deﬁne ui= Uji.
p
=1andui=−
pi/(1 −pi)ifXji=0.
=1ui.Userjisaccused(i.e.,j∈σ(y))if
> Z] < ǫ.
]whereeisthebaseofthenaturallogaindependenceoftherandom variablesuiwe

Y
E [eαui] .
eαui
=
i:yi=1
, where the ﬁrst inequality always holds, and
p
.7.Noticethatui≤
(1 −t)/t≤t−1/2
expectationzeroandvariance1weget

1 + αui + α2u2
i

= 1 + α2≤eα2.
E
u2
i

≤eα2m.
] ≤
eα2|{i:yi=1}|
have

eαS
αZ
≤eα2m−αZ.
<E
eαZ
= −⌈log(1/ǫ)⌉thus
] < e−k≤ǫ

---

### Page 11

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
P[C ∩σ(ρ(X
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
oﬀset,anditisenoughtomakeS> nZ
Wesetα = 1/(20c).Intheﬁrst
average E[e−αS
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
[n],n≤casthecodewordsoftheusers
bedistributedaccordingtothecodeFncǫ.
(p1, . . . , pm).Forsimplicityweintroduce
deﬁnitionUji= qiifXji= 1andUji= −1/qi
j=Pm
i=0yiUjiforj∈C.Let

,
(1)
yi
xiqi −n −xi
qi
number of ones in column i of X.Recall that
>Z.ThusifS>nZatleastonepirate
boundtheprobability
)) = ∅] ≤P[S≤nZ].
proofisasfollows.Ifthepirateswould
ofallzerosthenwewouldhaveS=0
accusenobody.Unfortunatelyforthe
iofXconsistsofallonestheymust
andthisdeﬁnitelyincreasesS.They
i where column
decreaseSifthecolumncontainsfewer
andincreaseSifthecolumncontains
knowthenumberxiofonesofthecolumn
thedistributionofpisuchthatthewins
theirchoiceforyihasalmostnoeﬀecton
ontheexponentialaverageE[e−αS]fora
allone columns isthusimpossible to
withveryhighprobability.
partoftheproofwestudytheexponential
] and in Equation (2) we ﬁnd the largest value it can take for any
proof we study that formula closely.We
whichMxinEquation(2)isthemaximum
x≤n −1.Thisrepresentsestablishing
onlyaminoreﬀectontheexpectation.
tocalculatingtheeﬀectonSoftheall
establishasimpleboundontheexponential
theprobabilityofS≤nZ(andthus
σ)usingtheMarkovinequality.

---

### Page 12

Usingtherulesofthesecondphase
"X

e−αS
= E
E
p,X
p
X
m
"
X
Y
=
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

X
Y
E
E
px
p,X[e−αS] =
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
p,X[e−αS] =
i
i=1
X
Theexpectationontherighthandside
Tosimplifytheexpression weletp
p
callywitheachpi,letq=
(1 −p)/p

E0,x= Ep
h
px(1 −
E1,x= Ep
Eachyiiseither0or1,furthermore
yi= 1bythemarkingcondition.Thus
X
E
p,X[e−αS] ≤
X
wheremax∗denotestheﬁrsttermE0
and themaximum of thetwo terms
notdependontheC-strategyρ,and
themarkingconditionwehaveequality
theproductonlydependsonxiand
wecanswitchthesummationandthe
expectationofe−αS.Itisstilltight
E
p,X[e−αS] ≤
ofthecodegenerationwehave
m
!#
Y

pxi
e−αS
i(1 −pi)n−xi
i=1
#

pxi
.
i(1 −pi)n−xi
=1
p in the ﬁrst phase or for
p and
phasesofgeneratingFncǫasindicated.
0-1 matrices X.The number of ones in column
(1)wehave
)#
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

X
Mx
,
(2)
x
x=0

---

### Page 13

where
M0= E0,0
Mx= max(E0,x, E1
We use eu≤1+u+u2that holds for
inE1,x.If−α(xq −(n −x)/q) < 1.7

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

px(1 −
F1,x= Ep
"
px(1 −p)n
F2,x= Ep

χx(p)(1
Rx= Ep
The term F1,xis the most important.
surethatitissmallfor1≤x≤n −
,
Mn= E1,n,
,x)for1 ≤x ≤n −1.
u < 1.7 to bound the exponential term
wehave

2

n −x
.
+ α2
xq −n −x
q
q
1−p
addingtheextra termχx(p)eα(n−x)/√
thecharacteristicfunctionoftheevent
by−α(xq −(n −x)/q) > 1.
version[15]ofthispaperwechoseα=
)<1alwayshold,thuswecouldmake
thetermχx(p).Unfortunately,thissmall
yieldasomewhat weaker error bound.This
enoughtoimplyCorollary3forhighc,
boundsachievablebythesemethods.
px(1 −p)n−x−

xq −n −x
αpx(1 −p)n−x
+
q
2

xq −n −x
+
α2px(1 −p)n−x
q
α(n−x)
√
χx(p)(1 −p)n−xe
1−p.
1,x + α2F2,x + Rx,

p)n−x
xq −n −x
,
q
2#

−x
≥0,
xq −n −x
q
α(n−x)

√
−p)n−xe
≥0.
1−p
Our choice of the distribution for p makes
1.Thespeciﬁcchoiceofthedistribution

---

### Page 14

isusedforthisboundonly.
Recall
r∈[t′, π/2 −t′],wheresin2t′= t.We
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

X
α2
x=0
Weboundeachtermseparately:
n
n
n

X
X
E0,x
=
x
x=0
x=0
=
Ep
=
Ep
thatp=sin2rwithauniformrandom
have1 −p = cos2r,q= cot rand
cos2n−2xr(x cot r −(n −x) tan r)dr.
f(r) = 1/2 sin2xr cos2n−2xr,
=tn−x(1 −t)x −tx(1 −t)n−x
.
π −4t′
0(nocutoﬀ)wouldbeoptimalyielding
t>0inothercalculationsofthisproof
Thechoicet=1/(300c)isacompromise
F1,x.For1 ≤x ≤n −1weuse
(1 −t)n−x
< 0
π −4t′
+ αtx(1 −t)n−x
+ α2F2,x + Rx.
π −4t′
,n=(1−t)n−tn
π−4t′
−t)n −tn
+ α2F2,n + Rn.
π −4t′
inEquation(2)

E0,x −
n

)n −Pn
tx(1 −t)n−x
x=1
x
+
π −4t′
n
n

n
X
Rx.
(3)
F2,x +
x
x
x=0
n

Ep
px(1 −p)n−x
x
"n
#
n

X
px(1 −p)n−x
x
x=0
[1] = 1;

---

### Page 15

n
n

X
tx(1 −t)
(1 −t)n−
x
x=1
n
n
n

n

X
X
E
F2,x
=
x
x
x=0
x=0
"n

X
=
Ep
x=0
Tofurthersimplifythisexpression
theindependentidenticallydistributed
P[Uj= q] = p and P[Uj= −1/q] = 1
variables have expectation 0 and variance 1, so we have
expectationisforaﬁxedpwithrespect
spellingoutthisexpectationyields
forpinthelastdisplayedequation.
n
n

X
F2
x
x=0
Forthelasterrorterm

χx(p
Rx= Ep
√
t/α
we have Rx= 0 for x > n−
call that choosing α
Forany 0 ≤x ≤nthefunction(1 −p
√
t/αthe
in[t, 1 −t],soforx ≤n −
forp ∈[t, 1 −t]isatp = 1 −α2(n −x
Rx≤e(α(
n

≤(ne
Using
x
n−x)n−xandnα ≤cα
√
t/α⌋
⌊n−
n
n

X
X
≤
Rx
x
x=0
x=0
√
⌊n−
t/α
X
=
e
x=0
√
⌊n−
t/α
X
<
e
x=0
√
<
3 · 19−⌈
n−x= 2(1 −t)n−1 ≥1 −2nt;
"

2#
px(1 −p)n−x
xq −n −x
p
q

2#
n
px(1 −p)n−x
xq −n −x
x
q
let0<p<1beﬁxedandconsider
randomvariablesUjforj∈[n]with
p
−p, where q=
(1 −p)/p.These random
E[(Pn
j=1Uj)2] = n.This
totherandomvariablesUj.Formally
exactlytheformulainsidetheexpectation
Thisimplies
,x= Ep[n] = n.

√
αn−x
)(1 −p)n−xe
1−p
as in this case χx(p) = 0 for p ∈[t, 1−t].(Resomewhat smaller we can get rid of this error term entirely.)
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

---

### Page 16

Nowwecanestimateeachtermin
n
n

X
Mx< 1 −α1 −2nt
x
π −4t′
x=0
Weusedn≤c,α=1/(20c)andt
inequalityaboveworksforc≥7only.
computeRxexactlytoprovethe
ByEquation(2)wehave
E
p,X[e−αS] < (1
BytheMarkovinequalityandm = 100
P[S≤nZ] ≤P[S≤cZ] ≤
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
accusedusers).HereΣ′= Σ ∪{?},
For∅̸ = C⊆[n]anunreadable digit C
submatrixofXformedbytherows
stringy=ρ(X)∈Σ′masoutputand
conditions.Forallpositions1≤i≤
digitsXjiwithj∈C.Furthermore,
agreethenyi̸=?.Wesaythatan
against coalitions of sizecifforanyC
digitC-strategyρtheerrorprobability
P[σ(ρ(X)) = ∅
isatmostǫ.
Equation(3):
√
t/α⌉< 1 −α/4.
+ α2n + 3 · 19−⌈
=1/(300c)here.Tobehonestthelast
Forsmallervaluesofconeneedsto
estimate.
−α/4)m< e−αm/4.
(4)
c2k,Z= 20ckweget
e−αm/4
e−αcZ= e−α(m/4−cZ)≤ǫc/4.
proof,ifS> nZthenC ∩σ(ρ(X))isnot
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
σ(y)⊆[n]:={1, 2, . . ., n}(thesetof
where?/∈Σrepresentstheunreadabledigit.
-strategyisanalgorithmρthattakesthe
withindicesinCasinput,andproducesa
satisﬁesthefollowing(strongmarking)
mthedigityiiseither?oroneofthe
ifforsomeiallthevaluesXjiforj∈C
unreadabledigitﬁngerprintcodeisǫ-secure
⊆[n]ofsize|C| ≤candanyunreadable
orσ(ρ(X))̸ ⊆C]

---

### Page 17

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
P[j∈σ(ρ(X))]
ρ
max
P[C ∩σ(ρ(X)) = ∅]
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
alphabetandletΣ′=Σ∪{?}forsome
Letusdenotebyfathetransformation
occurrenceof?byaandleavesallotherdigits
digit)ﬁngerprintcodeoverthealphabetΣ.
ﬁngerprintcode(X, σ ◦fa)where(X, σ)
ﬁngerprintcodeFoverthealphabetΣis
cthentheunreadablebitﬁngerprintcode
anycoalitionofsizec.Moreover,ifCis
arbitraryuserthenwehave
≥max
P[j∈σ′(ρ′(X))],
ρ′
≥max
P[C ∩σ′(ρ′(X)) = ∅],
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
Lindkvist [10] studied the relative power of ﬁngerprinting over binary and larger
severelylimitedclassofﬁngerprintcodes
asarbitraryalphabetsare.
Themain
5)answerboththesequestionsinfull
optimalcodelengthisthesame
ofﬁngerprinting andover an alphabet

---

### Page 18

TomakeourlowerboundinTheorem
theunreadabledigitmodel.ByLemma
Theorem5.LetFbeanunreadable
anarbitraryalphabetΣfornusers.
1/(100ca)areal,wherea > 1isa
(ii)below,then
m ≥da
whereda> 0dependssolelyona.
(i) For any coalitionC⊂[n] of size |
ρ,andanyuserℓ∈[n] \ C
P[ℓ∈
(ii)ForanycoalitionC⊆[n]of
strategyρ
P[C ∩σ(
IndependentofourpaperPeikert,
icallyalmostidenticallowerbound
Theirresultonlyappliestoalimited
thenumberofcolumntypes:the
Xproducedbythecode.Inthecode
numberof columntypeswasseverely limited.
matriceswithallthecolumnsdiﬀerent.
applicable.Nevertheless,someofthe
[11]andinthispaperaresimilarand
Astheproofusesanesoteric
divergence)wemotivatethechoice
Assumewehaveaﬁngerprintcode
ofTheorem5.Weconcentrateonthe
thepiratecoalitionCℓ=[c] \ {ℓ}
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
ThebiasfunctionmustgiveP[yi=
positionitosatisfythemarking
4workinbothmodelswestateitin
5.3Theorem4follows.
digitﬁngerprintcodeoflengthmover
Let3≤c≤nbeanintegerand0<ǫ<
constant.IfFsatisﬁestheconditions(i)and
c2log(1/ǫ),
C| = c−1, any unreadable digit C-strategy
σ(ρ(X))] ≤ǫ.
size|C|=candanyunreadabledigitC-
ρ(X)) = ∅] < 0.99
Shelat,andSmithin[11]proveanumerforthelengthofbinaryﬁngerprintcodes.
classofcodeswithastrongboundon
numberofnon-equalcolumnsofthematrix
constructedbyBonehandShaw[3]the
Ourconstruction typicallyyields
Forsuchcodestheboundin[11]isnot
techniquesofthelowerboundproofsin
weshallcommentonthesesimilarities.
measureofdistancefordistributions(R´enyi
here.
(X, σ)satisfyingconditions(i)and(ii)
set[c]oftheﬁrstcusersonly.Consider
containingalltheseusersbutuserℓ∈[c].
-strategyρℓtothiscoalitionsuchthatthe
thesameforallℓ∈[c].Herewethink
randomization comingfromtherandomized
not fullyjustiﬁed and willnot beused in the
distributionsofthetriples(X, σ, ρℓ(X))
useareverysimple.Wecallthistypeof
InabiasC-strategyρthepiratesdecide
ρ(X) if it is ? or the most popular digit si
yi= si is determined by a bias function
Cseesiatpositioniintheircodewords.
si]=1ifalloftheircodewordsagreeat
condition,whileifthemostpopulardigitis

---

### Page 19

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
Butform > cthisapproach gives
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
Alfr´ed R´enyi in[12].Ithasseldombeen
R´enyidivergencefromacommontarget
thecoalition of all cplayers bya
wehaveP[yi=?] = 1toaccommodatefor
isnotunique.
identicallydistributedoutputsρℓ(X)were
setσ(ρℓ(X))inthiscase?According
containanyoftheplayerswithprobability
containsoneofthemwithprobabilityat
ǫ < 1/(100c).Unfortunately, identical
asforℓ̸ =ℓ′thepiratecoalitionCℓand
mostpopulardigitatanygiven position.
by1.Thus,wehavetostudysomekind
The proof technique of [11] is almost identical to ours up to this point.They
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
P[yi=?].Thus,thedistributionofa
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
similar bias[c]-strategy.R´enyi divergence still

---

### Page 20

hasthepropertythateachdigit
simplyaddupfortheindependent
parameters conditions (i) and (ii) of Theorem 5
Ω(log(1/ǫ)) between ρ(X) and ρℓ(X
calculationintheproofofTheorem5.
Deﬁnition5.4.R´enyidivergenceof
randomvariablesQandRisdeﬁned
Hα+1(Q||R) =1
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
= Hα+1(Q1||
(b)
eαHα+1((Q,S)||(R,S))=
wheretheexpectationistaken
(c)Foranyfunctionf
Hα+1(f(Q)||
(d) If the random variables Q and R
P[R = 1] = s,0 < s < 1,then
Hα+1(Q||R
Furthermore,ifq/s < 10,(1 −q
Hα+1(Q||
wheretheconstanthiddeninthe
contributesO(1/c2),andthesecontributions
digits.Butwiththecorrectchoiceofthe
now implyatotal divergence of
) for at least one value of ℓ.See the detailed
orderα + 1(α>0)betweenthediscrete
as
X
!
(P[Q = x])α+1
,
(P[R = x])α
x
valuesxtakenbytherandomvariableQ
isonlydeﬁnedifallthesevaluesare
therandomvariableR.
onlyontheseparatedistributionsof
jointdistribution.Thefollowingbasic
wellknownandhavestraightforwardone
R1andR2areindependent,then
Q1, Q2)||(R1, R2))
R1) + Hα+1(Q2||R2).
E[eαHα+1((Q|S=s0)||(R|S=s0))],
forthevalues0oftherandomvariableS.
f(R)) ≤Hα+1(Q||R).
take values from {0, 1} and P[Q = 1] = q,
qα+1

.
) ≥1
αlog
sα
)/(1 −s) < 10,then

(q −s)2
,
R) = O
s(1 −s)
Onotationdependsonlyonα.

---

### Page 21

Usingthepropertiesabovewe
aboveformal.
ProofofTheorem5:Westartby
unreadable digit bias C-strategies the
ﬁrstcusersonly.Weapplycondition
probabilisticunreadabledigitCℓ-strategy
(ii) with the coalition C0= [c
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
(*)Iftherealsuandvsatisfy0<
f(u) ≤9f(v),1 −f(u) ≤9(1 −
(f(u) −f(
f(v)(1 −f
For0 ≤ℓ≤cand1≤i ≤mletk
amongthedigitsXjiwithj∈Cℓ,
multiplicity.
Wedeﬁnethebiasunreadabledigit
thefollowingrules.
ForﬁxedXand
independentlyfromyi∈{sℓ
i, ?}with

f

P[yi= sℓ
i] =
f

To check that ρℓisindeed an unreadable digit
markingcondition:ifkℓ
i= |Cℓ|then
positiveprobabilityonlyifsℓ
iisthe
j∈Cℓ,andinthiscasethereisno
Bycondition(ii)P[C∩σ(ρ0(X))
accordingtothedistributionFon(
maketheproofoftheTheorem5outlined
describingthepiratecoalitionsCandthe
proof isbased on.Weconcentrate on the
(i)forℓ∈[c],Cℓ=[c] \ {ℓ}andthe
ρℓdeﬁnedbelow.Weusecondition
] and the probabilistic unreadable digit C0-strategy
heretheunreadabledigitCℓ-strategies
fromthec>3case.Forρ0wetakethe
=ρ0(X),withithdigit(1≤i≤m)
ofthethreeindicesj∈C0andyi=?
distinct.Forρℓwithℓ∈[c]wetakethe
outputallowedforanunreadabledigit
otherwords,forℓ∈[c]thedigitsofthe
for1 ≤i ≤myi= sifXji= sforboth
forthetwoj∈Cℓ,thenyitakesone
probability1/3each.
ρℓforc > 3weneedsomepreparations.
byf(x) = 0ifx ≤0,f(x) = 3x2−2x3if
Thisfunctionwaschosenforthefollowing
v<1,u≤3vand1 −u≤3(1 −v)then
f(v))and
v))2

.
(u −v)2
(v))= O
ℓ
ibethemaximummultiplicityofadigit
andletsℓ
ibeoneofthedigitswiththis
Cℓ-strategyρℓfor0≤ℓ≤c≥4with
ℓ,thedigitsofy=ρℓ(X)arechosen

2kℓ
ifℓ> 0
i−c+1
c−1
 2k0

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
=∅]<0.99.
Heretheprobabilityis
X, σ)andaccordingtotherandomchoices

---

### Page 22

takeninρ0.Thusthereisauserj∈
more than 1/(100c).Assume
1andwehave
P[1 ∈σ(ρ0
Wecontrastthiswiththeboundgiven
P[1 ∈σ(
Ourgoalistoﬁnishtheproofby
enoughthenthedistributions(ρ0(X)
eachothertolettheseparationstated
Let α
ainthetheorem.
Letusﬁrstconsidertherandom
arbitraryﬁxedX.
Forc = 3itisstraightforward to
Hα+1(yi||y′
i) =
Ourﬁrstgoalistoproveasimilar
Supposec > 3.For1 ≤i ≤mwe
ifk0
i≥c/2 + 1inwhichcases0
iappears
digitsXjiforj∈C1,thuss0
iisan
Thus,bothyiandy′
itakevaluefrom
q= P[yi= s1
i] = f(q0
r= P[y′
i= s1
i] = f(r0
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

Hα+1(yi||y′
i) = O
The hidden constant in the O
onlyonαandthusontheexponenta
[c]accusedbyσ(ρ0(X))withprobability
without loss of generality thatthisistrue foruser
(X))] >
(5)
100c.
bycondition(i):
ρ1(X))] ≤ǫ.
(6)
showingthatifthecodeFisnotlong
, X, σ)and(ρ1(X), X, σ)aretoocloseto
inInequalities(5)and(6)happen.
be a positive parameter to be set later depending solely on the constant
variablesy= ρ0(X)andy′= ρ1(X)foran
see,that
O(1) = O(1/c2).
boundforc > 3.
haveyi∈{s0
i, ?}andP[yi= s0
i] > 0only
atleastk0
i−1 ≥c/2timesamongthe
absolutemajorityheretoo,ands1
i=s0
i.
{s1
i, ?}andbythedeﬁnition
i−c −1
,
)withq0=2k0
c −3
i−c + 1
)withr0=2k1
.
c −1
r=0impliesq=0andsimilarlyr=1
||y′
i)=0.Ifwehave0<r<1thenwe
−r0),thusproperty(*)ofthefunctionf
O((q0 −r0)2).
bound|q0−r0|=O(1/c).Usingthelast
theR´enyidivergenceweget

1

(q −r)2
= O
.
r(1 −r)
c2
notation here and elsewhere in this section depends
inthetheorem.

---

### Page 23

Nextweapplyproperty(a)ofthe
consider Xto beﬁxed,and thus all the
Sowehave
Hα+1(y||y
Ournextgoalistoconsider(X, σ
prove

Hα+1
(ρ0(X), X, σ)||(
Indeed,byproperty(b)oftheR´enyi
exponentialaverageofthecorresponding
Equation (7)boundsallthosedivergences,
andEquation(8)isveriﬁed.
Nowweapplyproperty(c)ofthe
g(y, X, σ) = χ1∈σ
thattellsifuser1isaccused.From
Hα+1(χ1∈σ(ρ0(X))||χ1∈σ(ρ1(X))) ≤Hα
Inequalities(5) and(6) andproperty (d)
lefthandsideisatleast

αlog
(100c)α+1ǫ
Thelastboundcan bemadetrueby
exponentintheǫ < 1/(100ca)condition
Puttingthelasttwodisplayed
m = Ω(
withtheconstantintheΩnotation
ConcludingRemarks
1.GuthandPﬁtzmannin[7]introduce
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

′) = O
.
(7)
c2
)tobedistributedaccordingtoFand

m

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

m
.
+1((ρ0(X), X, σ)||(ρ1(X), X, σ)) = O
c2
of theR´enyi divergence showthatthe

a −1
≥
α
2a + 10 log(1/ǫ).
settingα = 12/(a −1),wherea > 1isthe
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

---

### Page 24

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
ofsize|C| ≤(1 −2δ)c,andletρbeany
andPﬁtzmann.Wehave
P[C ∩σ(ρ(
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
andletδ< 1/2,letC⊆[n]beacoalition
C-strategyintherelaxedmodelofGuth
X)) = ∅] < ǫc/4,
thedistributionon(X, σ)deﬁnedbythe
forcoalitionsofsizecweonlyhaveto
(1 −2δ)⌉,acodethatisonlyaconstant
δ<1/2.Alsonoticethatforanybinary
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
codelengthisΩ(1/ǫb)forarbitraryb<2
Itiseasytoseethatifwechangethe
codeFnc′ǫ′withc′= ⌊2/ǫ⌋andǫ′= ǫ/2
withprobabilityǫ/2inadditionto
wegetaﬁngerprintcodesatisfyingthe
O(log(1/ǫ)/ǫ2).
philosophicalremarkonﬁngerprintingand
isacryptographicprimitivewhose

---

### Page 25

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
[1]G.R.Blakley, C.Meadows and G.
messages, Proc. of Crypto ’85
180–189.
[2]D.BonehandM.Franklin,An
Proc. of Crypto ’99
[3]D.BonehandJ.Shaw,
IEEETransactionsofInformation
[4]B.Chor,A.FiatandM.Naor,
839,Springer-VerlagBerlin,
[5]F.Chung,R.Graham,T.Leighton,
ofCombinatorics8(1),2001.
[6]A.Fiat,T.Tassa,Dynamictraitor
(2001),211–223.
[7]J.GuthandB.Pﬁtzmann,Errordigitaldata,InformationHiding
Berlin2000,pp.134-145.
[8]J.Kilian,T.Leighton,L.
Resistanceofdigitalwatermarks
1998IEEEInternationalSymposium
[9]K.KurosawaandY.Desmedt,
schemes, Advances in cryptology—EUROCRYPT’98
Berlin,1998,pp.145–157.
[10]T.Lindkvist,Fingerprintingdigital
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

---

### Page 26

[11]C.Peikert,A.Shelat,A.Smith,
printing,in:Proceedingsofthe
DiscreteAlgorithms(SODA)2003
[12]A.R´enyi,Probabilitytheory,
icsandMechanics,Vol.10.
London;AmericanElsevier
[13]R.Safavi-NainiandY.Wang,
Crypto’2000,LNCS1880,
316–332.
[14]J.N.Staddon,D.R.Stinson,R.
proof and traceability codes,
(2001),1042–1049.
[15]G.Tardos,Optimalprobabilistic
35thAnnualACMSymposium
125.
[16]T. Tassa, Low bandwidth dynamic traitor tracing schemes,
tology,toappear.
[17]Y.Yacobi,ImprovedBoneh-Shaw
cryptology—CT-RSA 2001
391.
[18]N. Wagner, Fingerprinting,
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
