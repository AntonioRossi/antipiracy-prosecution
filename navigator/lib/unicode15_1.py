"""Unicode 15.1.0 normalization data and NFC implementation.

The standard library binds :mod:`unicodedata` to the interpreter build, so
using it directly would make canonVersion c1 produce different bytes on older
supported Python runtimes.  This module vendors the canonical-decomposition,
canonical-combining-class, and composition tables from Unicode 15.1.0.

The data is a zlib-compressed, Base85-encoded varint stream.  Hangul
decomposition and composition are algorithmic under UAX #15 and are therefore
not duplicated in the payload.
"""

import base64
import zlib

UNICODE_VERSION = "15.1.0"

_DATA = (
    b"c-p<1d306BouJRX@423yv9s76<0T!^ojyIMd-{*boYVB2?z=QWYNNJ|(ip|T^N(I)#VEE>8Y2@tlZl=rq$dyv0RqG>J<x*C$"
    b"|kW05Qs$*AU3fH5JCuvec#M7_5Gyh;KZbJX3mT)zW2LTb?erxs#~|7^v(CBsvg7mzxnAkjE<*%^x@I3rs$t$`T651U;FdB|D"
    b"H~LR#UDC|FD=GnqNKqU76me;y%N;AU{tBe_BV(Hotm2#r(aNK7DxV8TavrJ@9+y>Jz&qc-|OfykNX&e8c#r@h#)q#!JS_`u{"
    b"&OzGJ*%4mMvkUNhx1^QG8lHTiqS5aatle8c#z@#p=q@fXHlex)5f&$xjO<J&*@#n;v8`Gey9DdtnB{?%U%>G`@ld-{%_4u0?"
    b"Qf5;xA@au0-vY+oTUVAFheD(mE&nWYEk(Sv#Uq1)`^B*6?KlxEIzqV8Uu-g71>v={Gezi{9_iexTsX}A*@eg|pM}H&_{7W_D"
    b"BWkqq-+!S$$N3HaxBb8IkNeR0(C~lbBSZfG<TK+lee}5@|Gy)b`fdkJHjf(rEoc~NhM8fgG=lygPg<lS{r#VAhw<+|Q`i1(h"
    b"tc+2q=9REI%SA|vEd)oW3=kYJ%c$eE$-<57~%iUGdj%EVf^q<et^u5|DdaWFXb1$Z~6aI&of8xA9S<-$@hY0w6EZIL-_3H_o"
    b")=~>4nXBuEX&47+xv3^J|;(HBHnjQ+s3~?fL)v(<@6*w_N>rWYvs3koyM)mj9kU>8TW5!aH!#@nzmuJLt*a$cfVpf8hV|4V8"
    b"P3%kA{a>e|WAFQbg8!x#J8`bW<E3*o;B^G*L>`{x<{@BSaP;U6P6|JVKm-;4fhzgvYm29{72S(^Udf7kHWEH++GQ$2s$D<m>"
    b"$_WC-Ev-)Vx@0~L1MR_~^O;7(oJm)X&ucyKLRH2OiX8c>E$~QZnu{uY7{_9hTTMhr;`oHP_N5A3wm&h4E)Q^tqd&mF0?<1YO"
    b"%J3QffAbl70ebE0Zp-`C!@Y*z>wC4w_&}ff(9rm;f1>6D|8%{;_|jQrp7Sj-{G<IZ`$zeUJ^pl4mYz}m6(0RjIrn#upY?T@T"
    b"kltfswgmwoquywHZ<~|w@c!ue*DkaxOl#9P=-8}lK*A2@r^(FGWyehJkPG@_i9Ug)+_U#F6caU{K(TA*&p>7XMA6Gr{n&x9^"
    b"bTYZ86MYsY)XV(m*;0fho!~hnMImh9WT(iJ?dgxv`|hk`_x^Y)BU#$+>Z4#E}t4Mx3ODl*f!GBc6<SGUBOaOi*V8$Ow=TAS1"
    b"vT0dfPh;ODd;ks^r{Nu)?3xk;oYk(NYS5-k|VxyfWClaWkDvZT?16f#oCNFgJIS|$bcX_MrBGq@xemPrJLl@fvBoc41toO6E"
    b";hG!9h;W<Pg8hntWuNFg9i6Dlm5<v`w6G04>CW08wNCa<E>4)G=3V#URr0|E}O*-O3FoGgu)ATiBxwj+`%Y~9aET<)bSgKC~"
    b"v02J%{wt^b61+t%AC>4kf15k{7`#o|$KY++@^OxO&Kya`I53ioabP65<8pL;aa=7K#BsG`5I2=*s&3jSP8$zKaoTt=igU+<c"
    b"ggq^yi0>V1@BViQ}8ZDJ_VyWoB&31IDw9h=YCT_JQq&^@mxFw#7`jt@w6oc#M1{U;5{xh5sU$oBx3a6r!Aj@_v!4<!TVhD^B"
    b"nb;X50d9Yk~TP8Bdh5K>fKnjNAZ-1xX+dB!hU60y+#D_)yqk1SJkioFj36nN*2W^^k0rlHI~$FDw!6kQBYb>n?bclRgA*fsf"
    b"?c++Q-d;GyJ2;W`g_GoORMWYpf|+8^@VjpUl+K$A4+oN$M*M|f0tPdF@>+Xch&h(HX7i6Dl<L=eki5{Tt63B+-j4B|LU2BSC"
    b"}4@Pk~9>jB)0^&JL0q+(w7r<yRp;)(k1a~twNBPWQj8i}!C|M^!yL8kY;bGxzVI0MhL8WwPm2eE0l%b}XjDfyY)0m}GLMo{K"
    b"i&6jF^Tt2<%u?xrJfEhq&M?e;B6F^=z{d)*M7Ug1%7o3Duj^bU*K%Qvq^}XK6V?k`q-4F6X%cRh^d{kM&F9Pm5+BgHe`n@LF"
    b"=qKuEO@h`f_h9db^M$;KZ-K*BsUzDsRrpdQ+?m8(;RHBk@Pik)+#xxUCvrBXVppWHeK>n^Hvlia9i_V%{fs#Q)@N9Va|}aS~"
    b"w#rBr(fszND<t^q5Eeq#qN`kuqzAbA{`q{Jf|PxnhR2HY71zENqZ6y;4J;utL)J2*YyLHepy&whg3Dl^B*t%1)`LT;dkZGSe"
    b")1;ou88`-MZAyM!e#9M){s@q9g3UOe=IX>Qg0ws}Ca-D{S<wDF}Vvs%+*uG0J~Ghb8RnsBagp|DU`BrF$JX?|?(e7WIe-I$k"
    b";y!<V*@a2s<F48p3D$UVm?VoM@GmlxP`2%x~rmj=CP}0jaFX)qBX@A9|+3*VSkyms@uWZzDk>)>`GY20TJk;DVxM8r)74Fa}"
    b"|I^&@YWu6dHaEX^_%)xoLsO@}*8ZBQ*{I`Yo$_0A$LkHR>$8MAUO)2sbUk!$G{0eL?t4S8N;)Rx^c&|)v+;ZDhCFY!YCdP~7"
    b"q$yeXufD}`Q93xd;NPizGrIQ`krCd4oMxNXPTy8r=$*f$(%Wa8Ws-WtU_V2uzUzL%ows}$S3CV?^k}m^E>9`p=*YkW|lBpI8"
    b"``J(`)8w{*Ad_QZ{OO%mz*U*hosF=BDS&Var(=z>j$3e+GUOCIUaIAp$$)**-6frqBl<nnE9dXbOD*qFG!%0MQjhV5Z4)GfO"
    b"zr3`#5;B{CC1Of?ZG_41sQ3IBzQ{6b#qOyv*32oA@B5nOmI7{T-%3r29^vGV$_Bm%Kin*{br`>zV$0v}046(51OxPgzr+Z=u"
    b"j)>`s{5WY>;$C6K@KL+nm#V6n$8ubZyhZ8>mBRL!gMshe#(x_k@7)b@=Dr5x?$_gBmI3zJ_l|I`eY?VISBm6P=l|)qjD=-R-"
    b"mx#-Z2gjw|CxoN8<aqEdg+2xEQs`4DX>xo**eN_C?6Tll;b<^HB2JkAMpNMgFq#{g0OFVNUIOuSdkTmrBL(!z9rOt=nB3(>;"
    b"ZNACd<K3(#h-!qxbcbLJ&I2R?@@Rnc#oz`1n*IJBKRqXzXm_0$ggDs&EX{3tgw~&9K28A&%ygN{&O%^?nSC+Ycz?S^%LC-`Z"
    b"=Ls01V3}0*x|SUBX7$nsf;pjckeg%cM&Tm)cynP?#onpDs+3(M=bonb{I&OPnro|GAlRu56EKMk0uzSR#m_P$FoS_FND)OM5"
    b"N|o25M$gw4{P3&J{SPrWdf%p?#?^+_NOBuhj_GB_l)-x3~@+HVODN$t0c{xazj!&a$%k8r7nvkHYvJ*g6>N}Mfmw#4ZY%bk0"
    b"|62o|qA`!(>K$X-~Ev%B7s)bcjQ?;kROuEGB5{D&*V<<QYjNx#Sq;bL|Foxoj()IqS#y3lLCbKnD9m)rVsZLPhpu~+5H_9Gp"
    b"mXPuxDVZ${Ny%(sNJ?f4*GTy_QhtV%%oEO#l6emM(0nPAFJ<OQZh>%~lqrxh>!i#&DYH~^3x!LiOrdb8T(M9%SIW<o@}*L;O"
    b"js%<%Y>y;vP@Vn<?E$<wUn$8R!hkmVYQU35f(`K0x4f7CF_NCQnFrH*I%=6vy|T~<+n)5t->u*a;x0q5-GDp%IuQd-NIc`X1"
    b"A1Sk}^$FrcHA93)`g3eqozjala-z(%G8FoK#^@*eJWoSwiaRlp4+mJEev*!cHl9roWe@e3_K*m6CnJUMblp?3I#z{k`O4Gri"
    b"Ks*b`Ow7(Jp&AN@>J<)cT4T7BFT(H<YIBHHWo=$Y3fGY_T-(}fwr$-+!wmM|pD7ETdP73K)138xElg-eBn!XjZ<xJ<ZQSS&0"
    b"NmI}*+D}?33mBI>PrLaoaDLf<W5}p-y3(pCAgy)65!am^z;YHyk;bq|!;Z<RcFH^`n@Y+C%v`5p_F(a|oZIUN8Q<x#7e=~hV"
    b"x|~t3d%D!1>@BHdozzh&b*z&*c1Ruha$d;Cb48Rb5jmUPRAErq|2$<1Gvu2PrDy1?)Jtv6zWygDQ<x#7#1x-tK9-suOHGfZr"
    b"Y0%ZB;{J9T(!RLR+*1mWj;1ZeJ#S}QhK?RUM{7l>(Yh&>wtX0o9r`;1dsVpZgsabf3Mu?ZmHmo-0BiJHOI%4C(4yb=NPLEkC"
    b"FDzhLQfy%T1%q=QZ9kj3y)5oH4wPEuiMh=4{O&W}BoO5+2a}dow+{PQP$NnjUki=Bs8{Q$M7dZ<re;eVedJ(syYNHf_Q)Ivi"
    b"x~iKa3OIG|gO&&eq_B)%!}9f|L1`pgFse<A5<F~sRH#F-LjY5u@0lDJe@CM?(dq4`kGeI(42^qDc#Su61>;cDR;P0I)+=vk3"
    b"a`%Uv?e4V=XyxEda5HQU>!hOR1!h^!Y!Xv_C!V|)i!qdVtnjW)T;vQkIrq8^psh@&``8wr>#5W|qE%9xM?@4@5;x8orLdS#6"
    b"9XfvATofn>e8VgcP-lg(N?0RYC0rw1C#)B45N;A~7H$pD!tE085bg@l!hHd*xG%uf4@i7K;=>XjmiVZ|M<qTX@reK}ES5U2O"
    b"3F3ib>R(7ulYzbZHC9#HP1ARTYC({XkMhFT?HEZPwK<kg&OBdG!||)2e7|ZAMOw9D63pYyEweFO{4FU#^fg&n{#yT`dp2Bc^"
    b"bKe8fk}g#)9J-$IfV+I<K)Qq%$rQX<T1LkwrS~cCkiAJB7P7DyVAlMvb=h`tagujXhKKVfRdp-A(%NXu6J;%+P4wqz~ur)ws"
    b"Zg9-h<K%f&O7=xAM->n_*WzFXtqVT~DF<NRffU@GOfS_ingK%=&jXsyPB4H`Mub-5=uG?sp$u{%qrWfW^Xp?&T78mDV$eS=2"
    b"lJ&ngy+Ql`RIk%CHy<4GilyY5l8nft^<0mw7Pia&=prsErT2|_E2WalpAg!YHtzh9TjRsn9ofh1tT<Tnnee{O(^JCgl&)}V3"
    b"r!jMjMixDO?E*bS7k@#6Hq$R<n>D6Uxb>LEy=ILfnz4<6KUGcVT;YBhtrgU~{)j%TUZSHAXFTS*=O*jJr8|kZMkQm}SHx+wI"
    b"k=y;+}F68!EI5?KIYJEZm_Xb<0cd75+m5uLZyuK3Oc)@oLRD3W9}x6y<h>S?O?{<WvX;7W&&?yK$(fD+coAh$YJ_)cb7(XAE"
    b"R(n;}%_am60jtv@6*f;iXI;#&Yg5PNVuwWlV1-YhzyI&Ue$k+jQ6$JGe_aqJfdV&EL|xx#{~Ak#1kVfzhJxYw7#GURuTTv4e"
    b"}RUZ!z}$*_xQHm_P^D&tW}BUjTob>yDest+@%`FNqm6>8qh%qeJz4ENr%G?K^fAvg1oo0-P58ls0PnIPHR(HA@#H}`35<@s3"
    b"1Bc4sGjxl5xuhD-GWX$y$ml?cDdh#9>lrQCyJcAdQtSjicsdU8lMy6C-WQJwZ<}x}lmr*?@bG(&Ca`95;!8s;PCfDt{NQXVv"
    b"*hd$i0j=D57qx6=p01~ni>RuNyPU@`K41X|Q{+e;&ptC^F1OV}(|TDCT5j{0-eK}H>$b2I6fl-Y=jhxmbm!VkrZO$f0>upNL"
    b"8fv$XH2G_7t>9v>BJ4(Z!3$;9(rTyERBPlv4w8hQm$X-$Eyv~xYeqoQ%w04%!p=|mW|BfQ{WuPWqjKi^9C-o>4`pVW{znZ_w"
    b"r4TQODptDm1;u)f&bUl-4p|Sb|Qmnyur`E14?inGt*BDPw%Q!G3ye5leICN_qoq;UO+%&FN-5u7KIht6m0gI?v1vu#acIi+P"
    b"pDO;2XD?$QVIQL~D8n6B_Jm9wN3F@kw4BMscvZm<iqfp%~bOyhp1gDtFFK}KfF-N=KO&04n=++ZF|=Fzy!2;R?#;0O!P4A%Q"
    b"ObbF8ytOo~KPeb!H*0LB$*PW$vo>XaUU>4uz@w+nFuV+q%?%iURxit(=FTIvZCpJk$+D`iK!SYD|9bUntA?gCh>BLoZ;&zs*"
    b"L!fIl9lKWJ0F&Vu=wtb>;L$ir7w@HuLtplDXJe$ZSMzLbXT@B&iwZzH18}P~@)}zJ+QEI6Iazn*(LKRa(Q+~}D2qEIBU5sf8"
    b")SH@&P68Sbp|SvM|=ZV#6q#;Qe<|X0JlIhtNa$w%Ba?SIZ$7)!ku^!8M1~i2kHQi&{f_-_or)YWsEXsMFwg!E9O1Wk{=m2c{"
    b"5$kkBs1yxseg9;{m(D2o|sa++lTmxH2-J^0=I+iVW@4>d5%cTpQV!G`B_R?gWR=Yb=_mhdfm`v>xnUre{D~y~e>u8rvH53DY"
    b";5(dMy1s|V?g-=KAa2AO?>whq!?ng%s$?!M#M+W)~(o6d)I!i}2yg$INOg@=TPh3%SpQzr2-;c?*!VTa_N5_U?;8HvwI+%0j"
    b"B#OH;*!am`JfveO@8#YUwo8_#{gIfRAEGYD@FZ7z`0{Q%=xm-Te_1C!~Z%L8YFl*&=q1W75>}@F43HtL$vG=OpmX>+fm+1uk"
    b"SzYFp<4tAWhlW{K?yV{(Lp~oVb4{(cy4G8KO>eo2eCLYvH=3gZpQnp_R|Y<>4t!o4_`E*wd85epo>?F6FTZ}^b3?fQyp02&`"
    b"uOU=vHslB>NPg;;MReypeRibapz)VU>)25(s)BXkk?dUWNq9B7ANUPCnsuPr91?>!CkO$iq5FlCC+m+jb)&Pq`5@PWYfjVVr"
    b"4k8aGVZ5ua^~~bY2^$^{E>Oc7Pk;F3A7oz<Tn#m04Dn$t=&A#gT2;?&8RjeH`2bkHC|!V&!bzrfWRr&FsofgR^sV+C`%4Ad{"
    b"EmVm2*xM7uyQC?f3+n8Av65S#@W<q^m#R}NNzMlh!`@(!6xw4dnK%E;^T3Jc-hD$>9-7RRYXwL~>wrMz&;bR%yN-36Jfn)5-"
    b"Cte>E?LKnFJF0EqGV@)jqM>*^vy7Gx$4fMYdOKroK*tJTZw2e3Q(RGns*G({Qt<HEtl*zm9AWL!)Q7~E0n=jviTk2^#=-xn0"
    b"Y;SsquE>`S@DQ9~C)Wk4ex=8Upp@O_CeR1Ebb9(Weda?QRP!2G1=a%jS~7E|o;Ht(YIZ~oAjsRTNZJN={<|K!b2|O_HoZo5k"
    b"#rH9)#>wjpX>ogz<m(p^|F4vp2On@UgwAQ=(Bec?cz1l+8BBNNc7;#mryNO2CBfRFE;@4MQ#Q!rUl?6s9{fZ2(+>1&1u)y*h"
    b"KV@v|gfg-eTS0`VpO5#H*}{!!l4gL3a{KkHI4L<#&lLO&Hj5Tmn-%^_gecd)#C1v747*!Dj<Ik&q6$Q*<x#+~tE*-iiy!tKj"
    b"R=v8=DWGYi2fa1d<cjj&tS@qk_8WN@G@vcb9Bt23t)Eg^080i*xz(MS+J$c`73@_jLUS(iOQH1F5?D!i0SuIr>jM0<784T2>"
    b"{A}{L=VA^e6V(NO02Sj_Z%QoKE(PlQnd%$_p=I~~3I3C$^$&0=Z+yj%@+b({fPg~7l6+5ykVAbaXTY;Tm|07-EK4q`4GdT5_"
    b"n|q?MgD+I|osr$b0x;))=-El|2;2n~Y?7C=0yeRqIGdrT;zD-b<ykr^?T&0O+CV5rr=_yd$Omht>%-YIG#;?;n9BEomA}!|5"
    b"!C&r|KCn_BOSeweaU3`UIrHYFFhyOpsbyzYiJ;vS>PY|&bowWYX+N^!X-Mb4s2hl@$k308L5#i%*{fbbORI=X{-W^+0iWd60"
    b"*yYO~KTw@?DI62+EfXU3f2Fg5-<7?19dbQM}SWu%De@p`#`soA`^MDlM|JZ3g?m!&+UWWK9HD*h!^j(248x;STmxyFm$Qscc"
    b"IQ@Ks>xWF9D@vmlinSLSA&dzL7e$r!T%OJlp-1Xhz)x?LC93661itcd|&kJhk5NBMl?eDEZ)WjnrGr-hp}Iyo$Dp@)f1_po*"
    b"1F{<T(N>5{-6`~fRHEU?@K3#YXn8gFN@O)$q%K(engJ0x~Jbo826)Xa)c<<Fn1U7*lu(91g@QZ^*Y$VTu3U-rWqD@5Svm##r"
    b"4wBZ)VJqkWYme#*E*{r7d`zQ!3bTr@z&F91DV%X$XLJ*-Jf)+P6gdNGPSfpYsDQ(^FMsuO9`u2-Y3xqHbhfu$(;^$)Qg9Ju@"
    b">{MWQ>m0F$T!6M9Ci|&1?Mm6YaHRL?J2M(hw&iVptlZ{*L7yk4JQ0Fh8HaTa*r(A<HP)RuJk_l$M>DBU;$g^yP)c^&d8XdN1"
    b"}yaS#1Q@7Rbd|mlj2~)(58Q_s?Z8o9~d<K_0()tDLUW77*33=RUHWUr&LD9NsU{$S>trU~_f3sr)V`e-^)^Dwh`Mv>pz(u}i"
    b"Pz#TaI*-c+PB<}cH@GMm>5=w#<UrBtWY=JU*zJwLFK7nFgu<vOj4ue__~@b=()ZwbE|Yy^+NUQFKVwa*W1{kQN7fJgOY6tI?"
    b"q^Xoa>s*Bv?aB`!Lrf=8CYtq=jZwuPz^AaU`3?}n^AQ#L58$fF7^A)~fscMTcEU2~`!_rivF)UqeGlqrKc4OES)np7WQ9F&8"
    b"RJF^9398*jOqyyoVnV9Lh)q?kMr=^+F=EryUL!W7_8BA7)qW!`RUI(mg6g0Vm!=LGap~%?5f@VJMtrI|X2b{8aU(uWoiO4<s"
    b">2u)R40u<s_HZXL3PFmq^T|=kgm=efspDp0#npE<L4#nypfoydX2=O>N674)CD6kq%Imssp^uE6jYauq%?KKND8T|#<+BK-A"
    b"GPVH;m+<x@jb*sar;Jy1H#7htwS-B~{%wQiAG%k&>pqFj7M5p)o0_9vPED>WMKdL#5)h260-`a9Y!GS~GB3C*!nc;<RSrw1#"
    b"k6vvFFd;IvM~Y0bfDorcpo9j7%Hr*$Sy>nxns**LBFIIVMVTIb@l&ckUfz-gV2)4Bksbs<jcBAnL6IIT-?T9@Lq7UHxP;k1T"
    b"vT9@IpF2`vt#c3_WX<dQST8`7Y5~sBSr?nENwF;-T8mDzNPU{++*0ngT>u_4@aaz~ov~Iv@-H6k=38%FIr*#`n>vo*hCY;tC"
    b"IITNzT6f{Jw&Jwz!D-!#)4C6*wGF3rKThi*oYuoQt?f9iM{rt?;<O&aX+4h9dIG1l1E=*QPU|V0*3&qxoj9#$a9X=?TF>INc"
    b"H^|3!)fisY3;*ly@1nt5vTPMPU~fy)+;!zS8-ae;j~`IX}y8ddK0Jh7EbGJoYp%yt#@%+@8PuG$7y|l)A|KY>qDH@M>wsIaa"
    b"xypk{75#Py7N^<w;qfsy)MU)E-YDNA2~*=BRz1q#V`eiOW&@J;^!hfG0jj9rUE+s6!r{*25m0)^-n0>k$u5>roF*>oE^b>v0"
    b"cG>j@7|YljD?^^^yv^|S}4wbO&sdd7p(+U3D%J?nWhNA-9<%u(k(Z{?_7&qq0`&l6XwE_jkl)kP0Z>m?6P>tzp4>lF`9>s8M"
    b"$bJR7@n?ZHU^I=fk_KZwb_dMhDGvUE$ec-`q{lbIO`p|>Z`pARR`q+ch`ouFVSEYIbxhm)#mZ#FZfjpJ&jmcFR-o#ur*&CCm"
    b"GQEj;D$5(2t3uwST$SyO%~MmnNqK6jH!fG@c$0J0G;ds<n(j@`Q@P$zxoU=Ye6Gs#j>=Orz2o!LEN^_Sn(a-=Rr%idJT=Fgl"
    b"Bec+-z`@2yq^}U0`KTzHQzg-SS|35$We>EV{_CJ@31UY><wh85^qe2D)lCos4_23>k2PUYq=Mvb)^@lwZa>hr7FG2S*ps5(^"
    b"~DtX|3^&$xyZ4Nf~OD7jt#84|6rshqW5=VXbESuvVw|uvT+?SgX^0SgW}{tkoGltko4htkrTK*6K<h)@p?hYqipcwOZxFTCM"
    b"hBtv36xR$F{ntF1n))jd9})xAEf)q_5))k8k4)zm1g)nF9XYI+pbYE~51YEBf^>a-}V)#*`Ks|8V5tMyS>t8GzOtNWv{Ru4v"
    b"DtsaTOTJ4C!T0I$swR$QFYxPbP*6Q6Ttktc4tkp(8)@qv{YjwXLYxRI1YxSTXYqi~vwR*&lwR+r-wR*yjwc6pwT0QB<T0P~*"
    b"T0QN@TJ7><t)BH`t#<pdR?qpdR(t$dtLOb#s~7xOs~7!PtC##(tC#&)t5^J3t5^M4tJnNktJnQlt2g{ut2g~vtGE1EtGE4Ft"
    b"M~j^tM~m#t3@v$t%hGfT3z-6((3XTkXDOdz**h$BF<{#i#V$XUqo3gdkJN=<|UNX)i0r-w!Dmj+WIms>8@9BNn2jQC2f5Le{"
    b"}X>{L$vY_@ga@@kd(+<B#ro6@PTgYxtu(U&9~W^&0+Y^K1B{EwAB^HouNP+VVR7XzT0fqsQMsAMJPpee~oT=%c6J!0RmjK3Z"
    b"qyP_)j_P_)h|L(w{OhN5*&ABxsFb0}KphM{Pkn}(uwZW)T!xpgR7=eD84ma9}Nuv`VLA7!aD>t|Ui-TF~jWmrE8tI5`nYE-8"
    b"6vl^9UVReQqtj=sJTEEh)5A-X|iVmwB>w~bGW<}Si>DC7|D%XlGQ8TO$N>rW|U7==LA5^GW7FOqM3#&8V!s?u3VRg>6Vk*=;"
    b"E3rZqSTWUVzLi+57FbxF3oWe9Mb^J$sm0bWveXjm%?!2F`Y=NkS|hSlku^3;g{=``wagkDR?DpsAysUR4XF}qgnq)UvHA(OM"
    b"pUX5*4Ro_ZpBusl~z)<s<5y+D=n<fD(fx%xLF?sRgLvlSk+n|h1DwSts1r3`lv>&vEB}=wbsXBwa&uoth2B>>#etI)OzdV8n"
    b"wZCyFzWWKCV!ktapN{!TKbqHe2sxsV&wgS!%2GPFOWspM=#mYh;$%ZjH-QP1eY;+F^|gtDV-!8nw$BSEF`YBP&$1HLgOnSXi"
    b"B{7FOpT3#)Ulh1I#w!s=|ZusZi!Se*wftj>ehkM*0=`jvijT0hQG?bffd)Dde`mO5&U&r-*%QDJr58Xs0CEUeBB3#;>_HL6C"
    b"Pvc}h_)7HCLs?+*3OP#Ua4XZBe)37>gVRd#}Se@rAtj-<_tMj~t)!A!db@o}Kv(yD^LYBH{jSj0z)`YOSY>lo_SF8y&>Z&!m"
    b"LS3^aRH*A#{4#aJN?E3ETJhEDmX%ViZd>sc>W-CCq3&8(o%bxP&ifWt=K~9?^9$=I>FS~NS-N^;{Uod&Tc3s16YD*_$k`K9R"
    b"nUGfsM73-dY!Z13#klyVn|K4-^)^&_QWieWxp3zA$ww2W!pd1v(x^yo}KnjLn_Dqbx2LK$7HGL_M|M8YrmhSX4s#nsXY7ru$"
    b"pOq9#*sL_iNN_`|}!=Z;!1}bL<HrHP@avMa{D(O;H6lR_6kHSXeE!17THY56f0Xb|71YZLH2^Hdg0y8>_R}#_BAwu{uj_tj;"
    b"nUt8;~o)md(1b*{9rIxB3f&Pp4rv&zQmthTW_Yiz8}S{ti#m5tT8+Q#Z!V`Fu$wXr(a*)d^NXD5bLy&aRS*4v5MYJ(k<t~T0"
    b"<>1vaW)!ATUb#At?I=9$Zom*|J&PE%nbDNFTx!uO<Y_hRBci32+JMGwPwaZS*R=e%kuxhrG!m7oN3#(Q;Ijr{BaoK9Got&-q"
    b"*;t)zHdg0;8>{nxjn#S3#_Bv|V|5<3u{zsrtj;4gR_9S0tMizR)p^{;>O5g%b#~ZTohNOq&Qms4=V=?Ov(v`vJY!>ZcG*~+X"
    b"YKf~>b6tD>YN>)t$OT~Y<1qo>g=_#I{R#_&I>kH=S3T<^OB9#dD+J5ykcW@UbV40ui03g*X=R-TYx<&Ro%45gw-v3Qdr%#$7"
    b"HKJ_M~ie*B+Cu?%9*l)qNYQGu6TB3_4hyX%1Frx`Wl3;b3)6cCb1#9jwkQ2dgvWV0C6YSe;WGtj?(pR%ecb)j7?<>YVOib>="
    b"!)oiiM)&O8UJbEbpUIm^N7ob6zB<~vxO^Bk<s0tc&ezJt}dz`^QV=wNj&a<Dp=I#`{B4pwK8gVh;!usWAHSe?rqtj=NwtFy$"
    b"x>MV7zI?Eia&J_+;XSsvbxzfSvtZ=Y8D;=!PDhI2x+QI6qaj-gT9jwk(4p!%C2di_9gVnj#!RlP+V0G3xSe^9_R_A&Lt8;^c"
    b")w$8Z>fGdDbv8Iyotqu3&MgjB=T--+v(dro+~#0)Zg;Rcn;fjpT@F^~ZU?Kg*}>{;aj-gD9jwkh4pwKIgVnj;!RkEVV09jJu"
    b"sRPpSe=I*tj=}^tMiD1)p^Xp>OA3Kb)IyvI!`-Tot+L==NSj9v&+HiJnLX}b~{*|=Nzog9tW%Qyo1%*>tJ>EIar++9IVcZ4p"
    b"!$S2dne4gVlM(!Rox~V0B(|FgkBI*qpZ<OwKzF7Uw+&gY$udz4_3=+)Q;bH-j$bW}1t+neJk4X1JJ}lU>ZsOc!%A%f;LbxtN"
    b">TF6QPG7jtu}i@BNOVs1`zF*m2Xn47sS=H?6+b2HDy+??rRZq9NsH)p$;oB1y0<{TGubFPcIInTx1EO0S5=ewAj3tY_2g)Zj"
    b"iA{TRWv5UF6#KqiP>SAsdx|o|qF6L&~#oS!xVs0*XF*l1{%*_%PbF<XN+$?i3H&?iro8>O%=1LcHv%<yPtaLFqt6a>@Y8P{}"
    b"#>L#Mbul+rxtN=)UChn3F6QPs7jv`D#oVlSF*nz{SeqMNjLoes#%807vANB~*xc@7Z0>L|Hg~!ho4Z_W&1M%<v(?4a+~Z<u?"
    b"sYLW_qmvwZ7!zfeiu{ofQzNs?qX>kaj`Uyx>%aWTrADwE{5hw7en)ui=lbi#n9|@F*MJ(7@A!!c4oJWoq5j1&g^lqGtax&nY"
    b"}J{W}l0ldBMfZyyRkLUUpG3Z@4I#H(iv>TP{lG9Tz3@u8Wd+&qc?4;G$wabWtwn4@bFNFdXHwayZK6p5Z8$dxxW3?i-GBnGu"
    b"b0nH`OCnG=n2xhxvxvN#&$a%(io<@RWl%bn3Em%F3wI@KACa@iG)a(Ox0s#8~@ojP?j8s+j@G|J`mXq3xa(I}U<qfsvJMWbB"
    b"ak4CvnjX}8##-Lng#GqVGjzPH$#h_ef$DmxUj6u1qh(Womj6u1qib1*Tj6u0P6N7Tu6@zklHU{PLLJZ2~#Tb;!OED;ymt#;Y"
    b"TN6+$_a>lNwk4og9!Nm3Jd}W9*`9!6c{BmV@^}J@Wk&*v<*5V|%gzK8%dP|z%X0}Rmgf^tEc+5rEUzV?SYA&+vAmgpVtFe8#"
    b"qv%9isjt|6wCVwD3%WrP%IxNpjbXiK(U-1K(SmLK(SmIK(VY0pjcK1P%LW$D3+@OD3)sjD3)~r6wCDi6w8eP6w8JHishC7ie"
    b"+N}#j+`YV!1PbV!1njV%ZizvD_a(u{;<+u{;z&v1|{ZSRM(WSRM<YSRN0cSat+ZEKdedEN=x+Ebj(TEbj$SEbj+UEFT0=EFT"
    b"B@|13Yh(A)oa`Gtkv{y)r@7kc~uFke~Z?f=VsRgt&<FY_(M-u^$$w-$T*|1`g$%-jFB`Hd26D)Tm!dHer3zrNht|JV5q<=+0"
    b"k&ezp?|2IMpz!("
)


def _read_varint(data, offset):
    value = 0
    shift = 0
    while True:
        if offset >= len(data):
            raise RuntimeError("truncated Unicode 15.1 normalization data")
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7f) << shift
        if byte < 0x80:
            return value, offset
        shift += 7
        if shift > 28:
            raise RuntimeError("invalid Unicode 15.1 normalization varint")


def _load_tables():
    data = zlib.decompress(base64.b85decode(_DATA))
    offset = 0

    count, offset = _read_varint(data, offset)
    combining = {}
    codepoint = 0
    for _ in range(count):
        delta, offset = _read_varint(data, offset)
        value, offset = _read_varint(data, offset)
        codepoint += delta
        combining[codepoint] = value

    count, offset = _read_varint(data, offset)
    decompositions = {}
    codepoint = 0
    for _ in range(count):
        delta, offset = _read_varint(data, offset)
        length, offset = _read_varint(data, offset)
        codepoint += delta
        sequence = []
        for _ in range(length):
            value, offset = _read_varint(data, offset)
            sequence.append(value)
        decompositions[codepoint] = tuple(sequence)

    count, offset = _read_varint(data, offset)
    compositions = {}
    for _ in range(count):
        first, offset = _read_varint(data, offset)
        second, offset = _read_varint(data, offset)
        composed, offset = _read_varint(data, offset)
        compositions[(first, second)] = composed

    if offset != len(data):
        raise RuntimeError("trailing Unicode 15.1 normalization data")
    if (len(combining), len(decompositions), len(compositions)) != (
            922, 2061, 941):
        raise RuntimeError("incomplete Unicode 15.1 normalization data")
    return combining, decompositions, compositions


_COMBINING, _DECOMPOSITIONS, _COMPOSITIONS = _load_tables()
del _DATA

_S_BASE = 0xAC00
_L_BASE = 0x1100
_V_BASE = 0x1161
_T_BASE = 0x11A7
_L_COUNT = 19
_V_COUNT = 21
_T_COUNT = 28
_N_COUNT = _V_COUNT * _T_COUNT
_S_COUNT = _L_COUNT * _N_COUNT


def _decompose(codepoint, output):
    syllable_index = codepoint - _S_BASE
    if 0 <= syllable_index < _S_COUNT:
        output.append(_L_BASE + syllable_index // _N_COUNT)
        output.append(_V_BASE + (syllable_index % _N_COUNT) // _T_COUNT)
        trailing = syllable_index % _T_COUNT
        if trailing:
            output.append(_T_BASE + trailing)
        return

    sequence = _DECOMPOSITIONS.get(codepoint)
    if sequence is None:
        output.append(codepoint)
        return
    for part in sequence:
        _decompose(part, output)


def _compose(first, second):
    leading_index = first - _L_BASE
    if 0 <= leading_index < _L_COUNT:
        vowel_index = second - _V_BASE
        if 0 <= vowel_index < _V_COUNT:
            return _S_BASE + (leading_index * _V_COUNT + vowel_index) * _T_COUNT

    syllable_index = first - _S_BASE
    trailing_index = second - _T_BASE
    if (0 <= syllable_index < _S_COUNT
            and syllable_index % _T_COUNT == 0
            and 0 < trailing_index < _T_COUNT):
        return first + trailing_index

    return _COMPOSITIONS.get((first, second))


def normalize_nfc(text):
    """Return *text* normalized to NFC using the pinned Unicode 15.1 tables."""
    if not isinstance(text, str):
        raise TypeError("normalize_nfc() argument must be str")

    decomposed = []
    for character in text:
        _decompose(ord(character), decomposed)

    # Canonical ordering is a stable insertion by combining class, bounded by
    # the preceding starter.  This avoids relying on runtime character data.
    ordered = []
    for codepoint in decomposed:
        combining = _COMBINING.get(codepoint, 0)
        position = len(ordered)
        if combining:
            while position:
                previous = _COMBINING.get(ordered[position - 1], 0)
                if previous == 0 or previous <= combining:
                    break
                position -= 1
        ordered.insert(position, codepoint)

    if not ordered:
        return ""

    result = [ordered[0]]
    starter_position = 0
    starter = ordered[0]
    last_combining = 0

    for codepoint in ordered[1:]:
        combining = _COMBINING.get(codepoint, 0)
        composed = _compose(starter, codepoint)
        if composed is not None and (
                last_combining == 0 or last_combining < combining):
            result[starter_position] = composed
            starter = composed
            continue

        if combining == 0:
            starter_position = len(result)
            starter = codepoint
        last_combining = combining
        result.append(codepoint)

    return "".join(chr(codepoint) for codepoint in result)
