---
id: supported
title: Supported Functions
---
This is a list of TeX functions supported by KaTeX. It is sorted into logical groups.

There is a similar [Support Table](support_table.md), sorted alphabetically, that lists both supported and un-supported functions.

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.25/dist/katex.min.css" integrity="sha384-WcoG4HRXMzYzfCgiyfrySxx90XSl2rxY5mnVY5TwtWE6KLrArNKn0T/mOgNL0Mmi" crossorigin="anonymous">
<style>
p {overflow-wrap: break-word;}
table tr,
table td {
    vertical-align: middle;
    overflow-wrap: break-word;
}
</style>

<div class="katex-hopscotch">

## Accents

||||
|:----------------------------|:----------------------------------------------------|:------
|$a'$ `a'`  |$\tilde{a}$ `\tilde{a}`|$\mathring{g}$ `\mathring{g}`
|$a''$ `a''`|$\widetilde{ac}$ `\widetilde{ac}`  |$\overgroup{AB}$ `\overgroup{AB}`
|$a^{\prime}$ `a^{\prime}` |$\utilde{AB}$ `\utilde{AB}`  |$\undergroup{AB}$ `\undergroup{AB}`
|$\acute{a}$ `\acute{a}`|$\vec{F}$ `\vec{F}` |$\Overrightarrow{AB}$ `\Overrightarrow{AB}`
|$\bar{y}$ `\bar{y}` |$\overleftarrow{AB}$ `\overleftarrow{AB}`|$\overrightarrow{AB}$ `\overrightarrow{AB}`
|$\breve{a}$ `\breve{a}`|$\underleftarrow{AB}$ `\underleftarrow{AB}` |$\underrightarrow{AB}$ `\underrightarrow{AB}`
|$\check{a}$ `\check{a}`|$\overleftharpoon{ac}$ `\overleftharpoon{ac}`  |$\overrightharpoon{ac}$ `\overrightharpoon{ac}`
|$\dot{a}$ `\dot{a}` |$\overleftrightarrow{AB}$ `\overleftrightarrow{AB}`  |$\overbrace{AB}$ `\overbrace{AB}`
|$\ddot{a}$ `\ddot{a}`  |$\underleftrightarrow{AB}$ `\underleftrightarrow{AB}`|$\underbrace{AB}$ `\underbrace{AB}`
|$\dddot{a}$ `\dddot{a}`|$\overline{AB}$ `\overline{AB}` |$\overlinesegment{AB}$ `\overlinesegment{AB}`
|$\ddddot{a}$ `\ddddot{a}`|$\underline{AB}$ `\underline{AB}`  |$\underlinesegment{AB}$ `\underlinesegment{AB}`
|$\grave{a}$ `\grave{a}`|$\widecheck{ac}$ `\widecheck{ac}`  |$\underbar{X}$ `\underbar{X}`
|$\hat{\theta}$ `\hat{\theta}`|$\widehat{ac}$ `\widehat{ac}`||

***Accent functions inside \\text{…}***

|||||
|:---------------------|:---------------------|:---------------------|:-----
|$\text{\'{a}}$ `\'{a}`|$\text{\~{a}}$ `\~{a}`|$\text{\.{a}}$ `\.{a}`|$\text{\H{a}}$ `\H{a}`
|$\text{\`{a}}$ <code>\\`{a}</code>|$\text{\={a}}$ `\={a}`|$\text{\"{a}}$ `\"{a}`|$\text{\v{a}}$ `\v{a}`
|$\text{\^{a}}$ `\^{a}`|$\text{\u{a}}$ `\u{a}`|$\text{\r{a}}$ `\r{a}`|

See also [letters and unicode](#letters-and-unicode).

## Delimiters

||||||
|:-----------------------------------|:---------------------------------------|:----------|:-------------------------------------------------------|:-----
|$(~)$ `( )` |$\lparen~\rparen$ `\lparen`<br>$~~~~$`\rparen`|$⌈~⌉$ `⌈ ⌉`|$\lceil~\rceil$ `\lceil`<br>$~~~~~$`\rceil`  |$\uparrow$ `\uparrow`
|$[~]$ `[ ]` |$\lbrack~\rbrack$ `\lbrack`<br>$~~~~$`\rbrack`|$⌊~⌋$ `⌊ ⌋`|$\lfloor~\rfloor$ `\lfloor`<br>$~~~~~$`\rfloor` |$\downarrow$ `\downarrow`
|$\{ \}$ `\{ \}`|$\lbrace \rbrace$ `\lbrace`<br>$~~~~$`\rbrace`|$⎰⎱$ `⎰⎱`  |$\lmoustache \rmoustache$ `\lmoustache`<br>$~~~~$`\rmoustache`|$\updownarrow$ `\updownarrow`
|$⟨~⟩$ `⟨ ⟩` |$\langle~\rangle$ `\langle`<br>$~~~~$`\rangle`|$⟮~⟯$ `⟮ ⟯`|$\lgroup~\rgroup$ `\lgroup`<br>$~~~~~$`\rgroup` |$\Uparrow$ `\Uparrow`
|$\vert$ <code>&#124;</code> |$\vert$ `\vert` |$┌ ┐$ `┌ ┐`|$\ulcorner \urcorner$ `\ulcorner`<br>$~~~~$`\urcorner`  |$\Downarrow$ `\Downarrow`
|$\Vert$ <code>&#92;&#124;</code> |$\Vert$ `\Vert` |$└ ┘$ `└ ┘`|$\llcorner \lrcorner$ `\llcorner`<br>$~~~~$`\lrcorner`  |$\Updownarrow$ `\Updownarrow`
|$\lvert~\rvert$ `\lvert`<br>$~~~~$`\rvert`|$\lVert~\rVert$ `\lVert`<br>$~~~~~$`\rVert` |`\left.`|  `\right.` |$\backslash$ `\backslash`
|$\lang~\rang$ `\lang`<br>$~~~~$`\rang`|$\left\lt~\right\gt$ `\lt \gt`|$⟦~⟧$ `⟦ ⟧`|$\llbracket~\rrbracket$ `\llbracket`<br>$~~~~$`\rrbracket`|$/$ `/`
|$\lBrace~\rBrace$ `\lBrace \rBrace`

**Delimiter Sizing**

$\left(\LARGE{AB}\right)$ `\left(\LARGE{AB}\right)`

$( \big( \Big( \bigg( \Bigg($ `( \big( \Big( \bigg( \Bigg(`

||||||
|:--------|:------|:--------|:-------|:------|
|`\left`  |`\big` |`\bigl`  |`\bigm` |`\bigr`
|`\middle`|`\Big` |`\Bigl`  |`\Bigm` | `\Bigr`
|`\right` |`\bigg`|`\biggl` |`\biggm`|`\biggr`
|         |`\Bigg`|`\Biggl` |`\Biggm`|`\Biggr`

</div>

## Environments

<div class="katex-cards" id="environments">

|||||
|:---------------------|:---------------------|:---------------------|:--------
|$\begin{matrix} a & b \\ c & d \end{matrix}$ | `\begin{matrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{matrix}` |$\begin{array}{cc}a & b\\c & d\end{array}$ | `\begin{array}{cc}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{array}`
|$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ |`\begin{pmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{pmatrix}` |$\begin{bmatrix} a & b \\ c & d \end{bmatrix}$ | `\begin{bmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{bmatrix}`
|$\begin{vmatrix} a & b \\ c & d \end{vmatrix}$ |`\begin{vmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{vmatrix}` |$\begin{Vmatrix} a & b \\ c & d \end{Vmatrix}$ |`\begin{Vmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{Vmatrix}`
|$\begin{Bmatrix} a & b \\ c & d \end{Bmatrix}$ |`\begin{Bmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{Bmatrix}`|$\def\arraystretch{1.5}\begin{array}{c:c:c} a & b & c \\ \hline d & e & f \\ \hdashline g & h & i \end{array}$|`\def\arraystretch{1.5}`<br>&nbsp;&nbsp;&nbsp;`\begin{array}{c:c:c}`<br>&nbsp;&nbsp;&nbsp;`a & b & c \\ \hline`<br>&nbsp;&nbsp;&nbsp;`d & e & f \\`<br>&nbsp;&nbsp;&nbsp;`\hdashline`<br>&nbsp;&nbsp;&nbsp;`g & h & i`<br>`\end{array}`
|$x = \begin{cases} a &\text{if } b \\ c &\text{if } d \end{cases}$ |`x = \begin{cases}`<br>&nbsp;&nbsp;&nbsp;`a &\text{if } b  \\`<br>&nbsp;&nbsp;&nbsp;`c &\text{if } d`<br>`\end{cases}`|$\begin{rcases} a &\text{if } b \\ c &\text{if } d \end{rcases}⇒…$ |`\begin{rcases}`<br>&nbsp;&nbsp;&nbsp;`a &\text{if } b  \\`<br>&nbsp;&nbsp;&nbsp;`c &\text{if } d`<br>`\end{rcases}⇒…`|
|$\begin{smallmatrix} a & b \\ c & d \end{smallmatrix}$ | `\begin{smallmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{smallmatrix}` |$$\sum_{\begin{subarray}{l} i\in\Lambda\\  0<j<n\end{subarray}}$$ | `\sum_{`<br>`\begin{subarray}{l}`<br>&nbsp;&nbsp;&nbsp;`i\in\Lambda\\`<br>&nbsp;&nbsp;&nbsp;`0<j<n`<br>`\end{subarray}}`|

The auto-render extension will render the following environments even if they are not inside math delimiters such as `$$…$$`. They are display-mode only.

<style>
  #env + table tr td:nth-child(1) { min-width: 11em }
  #env + table tr td:nth-child(3) { min-width: 13em }
</style>
<div id="env"></div>

|||||
|:---------------------|:---------------------|:---------------------|:--------
|$$\begin{equation}\begin{split}a &=b+c\\&=e+f\end{split}\end{equation}$$ |`\begin{equation}`<br>`\begin{split}`&nbsp;&nbsp;&nbsp;`a &=b+c\\`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`&=e+f`<br>`\end{split}`<br>`\end{equation}` |$$\begin{align} a&=b+c \\ d+e&=f \end{align}$$ |`\begin{align}`<br>&nbsp;&nbsp;&nbsp;`a&=b+c \\`<br>&nbsp;&nbsp;&nbsp;`d+e&=f`<br>`\end{align}` |
|$$\begin{gather} a=b \\ e=b+c \end{gather}$$ |`\begin{gather}`<br>&nbsp;&nbsp;&nbsp;`a=b \\ `<br>&nbsp;&nbsp;&nbsp;`e=b+c`<br>`\end{gather}`|$$\begin{alignat}{2}10&x+&3&y=2\\3&x+&13&y=4\end{alignat}$$ | `\begin{alignat}{2}`<br>&nbsp;&nbsp;&nbsp;`10&x+&3&y=2\\`<br>&nbsp;&nbsp;&nbsp;`3&x+&13&y=4`<br>`\end{alignat}`
|$$\begin{CD}A @>a>> B \\@VbVV @AAcA\\C @= D\end{CD}$$ | `\begin{CD}`<br>&nbsp;&nbsp;&nbsp;`A  @>a>>  B  \\`<br>`@VbVV    @AAcA \\`<br>&nbsp;&nbsp;&nbsp;`C  @=   D`<br>`\end{CD}`

#### Other KaTeX Environments

| Environments | How they differ from those shown above |
|:-----------------------------------------------|:------------------|
| `darray`, `dcases`, `drcases`                  | … apply `displaystyle` |
| `matrix*`, `pmatrix*`, `bmatrix*`<br>`Bmatrix*`, `vmatrix*`, `Vmatrix*` | … take an optional argument to set column<br>alignment, as in `\begin{matrix*}[r]`
| `equation*`, `gather*`<br>`align*`, `alignat*` | … have no automatic numbering. Alternatively, you can use `\nonumber` or `\notag` to omit the numbering for a specific row of the equation. |
| `gathered`, `aligned`, `alignedat`             | … do not need to be in display mode.<br> … have no automatic numbering.<br> … must be inside math delimiters in<br>order to be rendered by the auto-render<br>extension. |

</div>

Acceptable line separators include: `\\`, `\cr`, `\\[distance]`, and `\cr[distance]`. *Distance* can be written with any of the [KaTeX units](#units).

The `{array}` environment supports `|` and `:` vertical separators.

The `{array}` environment does not yet support `\cline` or `\multicolumn`.

`\tag` can be applied to individual rows of top-level environments
(`align`, `align*`, `alignat`, `alignat*`, `gather`, `gather*`).

<div class="katex-hopscotch">

## HTML

The following "raw HTML" features are potentially dangerous for untrusted
inputs, so they are disabled by default, and attempting to use them produces
the command names in red (which you can configure via the `errorColor`
[option](options.md)).  To fully trust your LaTeX input, you need to pass
an option of `trust: true`; you can also enable just some of the commands
or for just some URLs via the `trust` [option](options.md).

|||
|:----------------|:-------------------|
| $\href{https://katex.org/}{\KaTeX}$ | `\href{https://katex.org/}{\KaTeX}` |
| $\url{https://katex.org/}$ | `\url{https://katex.org/}` |
| $\includegraphics[height=0.8em, totalheight=0.9em, width=0.9em, alt=KA logo]{https://katex.org/img/khan-academy.png}$ | `\includegraphics[height=0.8em, totalheight=0.9em, width=0.9em, alt=KA logo]{https://katex.org/img/khan-academy.png}` |
| $\htmlId{bar}{x}$ <code>…&lt;span id="bar" class="enclosing"&gt;…x…&lt;/span&gt;…</code> | `\htmlId{bar}{x}` |
| $\htmlClass{foo}{x}$ <code>…&lt;span class="enclosing foo"&gt;…x…&lt;/span&gt;…</code> | `\htmlClass{foo}{x}` |
| $\htmlStyle{color: red;}{x}$ <code>…&lt;span style="color: red;" class="enclosing"&gt;…x…&lt;/span&gt;…</code> | `\htmlStyle{color: red;}{x}` |
| $\htmlData{foo=a, bar=b}{x}$ <code>…&lt;span data-foo="a" data-bar="b" class="enclosing"&gt;…x…&lt;/span&gt;…</code> | `\htmlData{foo=a, bar=b}{x}` |

`\includegraphics` supports `height`, `width`, `totalheight`, and `alt` in its first argument. `height` is required.

HTML extension (`\html`-prefixed) commands are non-standard, so loosening `strict` option for `htmlExtension` is required.


## Letters and Unicode

**Greek Letters**

Direct Input: $Α Β Γ Δ Ε Ζ Η Θ Ι \allowbreak Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω$
$\allowbreak α β γ δ ϵ ζ η θ ι κ λ μ ν ξ o π \allowbreak ρ σ τ υ ϕ χ ψ ω ε ϑ ϖ ϱ ς φ ϝ$

|||||
|---------------|-------------|-------------|---------------|
| $\Alpha$ `\Alpha` | $\Beta$ `\Beta` | $\Gamma$ `\Gamma`| $\Delta$ `\Delta`
| $\Epsilon$ `\Epsilon` | $\Zeta$ `\Zeta` | $\Eta$ `\Eta` | $\Theta$ `\Theta`
| $\Iota$ `\Iota` | $\Kappa$ `\Kappa` | $\Lambda$ `\Lambda` | $\Mu$ `\Mu`
| $\Nu$ `\Nu` | $\Xi$ `\Xi` | $\Omicron$ `\Omicron` | $\Pi$ `\Pi`
| $\Rho$ `\Rho` | $\Sigma$ `\Sigma` | $\Tau$ `\Tau` | $\Upsilon$ `\Upsilon`
| $\Phi$ `\Phi` | $\Chi$ `\Chi` | $\Psi$ `\Psi` | $\Omega$ `\Omega`
| $\varGamma$ `\varGamma`| $\varDelta$ `\varDelta` | $\varTheta$ `\varTheta` | $\varLambda$ `\varLambda`  |
| $\varXi$ `\varXi`| $\varPi$ `\varPi` | $\varSigma$ `\varSigma` | $\varUpsilon$ `\varUpsilon` |
| $\varPhi$ `\varPhi`  | $\varPsi$ `\varPsi`| $\varOmega$ `\varOmega` ||
| $\alpha$ `\alpha`| $\beta$ `\beta`  | $\gamma$ `\gamma` | $\delta$ `\delta`|
| $\epsilon$ `\epsilon` | $\zeta$ `\zeta`  | $\eta$ `\eta`| $\theta$ `\theta`|
| $\iota$ `\iota` | $\kappa$ `\kappa` | $\lambda$ `\lambda`| $\mu$ `\mu`|
| $\nu$ `\nu`| $\xi$ `\xi` | $\omicron$ `\omicron`  | $\pi$ `\pi`|
| $\rho$ `\rho`  | $\sigma$ `\sigma` | $\tau$ `\tau`| $\upsilon$ `\upsilon` |
| $\phi$ `\phi`  | $\chi$ `\chi`| $\psi$ `\psi`| $\omega$ `\omega`|
| $\varepsilon$ `\varepsilon` | $\varkappa$ `\varkappa` | $\vartheta$ `\vartheta` | $\thetasym$ `\thetasym`
| $\varpi$ `\varpi`| $\varrho$ `\varrho`  | $\varsigma$ `\varsigma` | $\varphi$ `\varphi`
| $\digamma $ `\digamma`

**Other Letters**

||||||
|:----------|:----------|:----------|:----------|:----------|
|$\imath$ `\imath`|$\nabla$ `\nabla`|$\Im$ `\Im`|$\Reals$ `\Reals`|$\text{\OE}$ `\text{\OE}`
|$\jmath$ `\jmath`|$\partial$ `\partial`|$\image$ `\image`|$\wp$ `\wp`|$\text{\o}$ `\text{\o}`
|$\aleph$ `\aleph`|$\Game$ `\Game`|$\Bbbk$ `\Bbbk`|$\weierp$ `\weierp`|$\text{\O}$ `\text{\O}`
|$\alef$ `\alef`|$\Finv$ `\Finv`|$\N$ `\N`|$\Z$ `\Z`|$\text{\ss}$ `\text{\ss}`
|$\alefsym$ `\alefsym`|$\cnums$ `\cnums`|$\natnums$ `\natnums`|$\text{\aa}$ `\text{\aa}`|$\text{\i}$ `\text{\i}`
|$\beth$ `\beth`|$\Complex$ `\Complex`|$\R$ `\R`|$\text{\AA}$ `\text{\AA}`|$\text{\j}$ `\text{\j}`
|$\gimel$ `\gimel`|$\ell$ `\ell`|$\Re$ `\Re`|$\text{\ae}$ `\text{\ae}`
|$\daleth$ `\daleth`|$\hbar$ `\hbar`|$\real$ `\real`|$\text{\AE}$ `\text{\AE}`
|$\eth$ `\eth`|$\hslash$ `\hslash`|$\reals$ `\reals`|$\text{\oe}$ `\text{\oe}`

Direct Input: $∂ ∇ ℑ Ⅎ ℵ ℶ ℷ ℸ ⅁ ℏ ð − ∗$
ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝÞßàáâãäåçèéêëìíîïðñòóôöùúûüýþÿ
₊₋₌₍₎₀₁₂₃₄₅₆₇₈₉ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓᵦᵧᵨᵩᵪ⁺⁻⁼⁽⁾⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘʷˣʸᶻᵛᵝᵞᵟᵠᵡ

Math-mode Unicode (sub|super)script characters will render as if you had written regular characters in a subscript or superscript. For instance, `A²⁺³` will render the same as `A^{2+3}`.

</div>
<div class="katex-cards" id="math-alpha">

**Unicode Mathematical Alphanumeric Symbols**

| Item        |  Range              |  Item             |  Range  |
|-------------|---------------------|-------------------|---------------|
| Bold        | $\text{𝐀-𝐙 𝐚-𝐳 𝟎-𝟗}$  | Double-struck     | $\text{𝔸-}ℤ\ 𝕜$
| Italic      | $\text{𝐴-𝑍 𝑎-𝑧}$      | Sans serif        | $\text{𝖠-𝖹 𝖺-𝗓 𝟢-𝟫}$
| Bold Italic | $\text{𝑨-𝒁 𝒂-𝒛}$      | Sans serif bold   | $\text{𝗔-𝗭 𝗮-𝘇 𝟬-𝟵}$
| Script      | $\text{𝒜-𝒵}$         | Sans serif italic | $\text{𝘈-𝘡 𝘢-𝘻}$
| Fraktur     | $\text{$𝔄$-$ℨ$}\text{ $𝔞$-$𝔷$}$| Monospace        | $\text{𝙰-𝚉 𝚊-𝚣 𝟶-𝟿}$
| Bold Fraktur | $\text{𝕬-𝖅 𝖆-𝖟}$ | |

</div>
<div class="katex-hopscotch">

**Unicode**

The letters listed above will render properly in any KaTeX rendering mode.

In addition, Armenian, Brahmic, Georgian, Chinese, Japanese, and Korean glyphs are always accepted in text mode. However, these glyphs will be rendered from system fonts (not KaTeX-supplied fonts) so their typography may clash.
You can provide rules for CSS classes `.latin_fallback`, `.cyrillic_fallback`, `.brahmic_fallback`, `.georgian_fallback`, `.cjk_fallback`, and `.hangul_fallback` to provide fallback fonts for these languages.
Use of these glyphs may cause small vertical alignment issues: KaTeX has detailed metrics for listed symbols and most Latin, Greek, and Cyrillic letters, but other accepted glyphs are treated as if they are each as tall as the letter M in the current KaTeX font.

If the KaTeX rendering mode is set to `strict: false` or `strict: "warn"` (default), then KaTeX will accept all Unicode letters in both text and math mode.
All unrecognized characters will be treated as if they appeared in text mode, and are subject to the same issues of using system fonts and possibly using incorrect vertical alignment.

For Persian composite characters, a user-supplied [plug-in](https://github.com/HosseinAgha/persian-katex-plugin) is under development.

Any character can be written with the `\char` function and the Unicode code in hex. For example `\char"263a` will render as $\char"263a$.

## Layout

### Annotation

|||
|:------------------------------|:-----
|$\cancel{5}$ `\cancel{5}`|$\overbrace{a+b+c}^{\text{note}}$ `\overbrace{a+b+c}^{\text{note}}`
|$\bcancel{5}$ `\bcancel{5}` |$\underbrace{a+b+c}_{\text{note}}$ `\underbrace{a+b+c}_{\text{note}}`
|$\xcancel{ABC}$ `\xcancel{ABC}`|$\not =$ `\not =`
|$\sout{abc}$ `\sout{abc}`|$\boxed{\pi=\frac c d}$ `\boxed{\pi=\frac c d}`
|$a_{\angl n}$ `$a_{\angl n}`|$a_\angln$ `a_\angln`
|$\phase{-78^\circ}$`\phase{-78^\circ}` |

`\tag{hi} x+y^{2x}`
$$\tag{hi} x+y^{2x}$$

`\tag*{hi} x+y^{2x}`
$$\tag*{hi} x+y^{2x}$$

### Line Breaks

KaTeX 0.10.0+ will insert automatic line breaks in inline math after relations or binary operators such as “=” or “+”. These can be suppressed by `\nobreak` or by placing math inside a pair of braces, as in `{F=ma}`. `\allowbreak` will allow automatic line breaks at locations other than relations or operators.

Hard line breaks are `\\` and `\newline`.

In display math, KaTeX does not insert automatic line breaks. It ignores display math hard line breaks when rendering option `strict: true`.

### Vertical Layout

||||
|:--------------|:----------------------------------------|:-----
|$x_n$ `x_n` |$\stackrel{!}{=}$ `\stackrel{!}{=}`| $a \atop b$ `a \atop b`
|$e^x$ `e^x` |$\overset{!}{=}$ `\overset{!}{=}`  | $a\raisebox{0.25em}{$b$}c$ `a\raisebox{0.25em}{$b$}c`
|$_u^o $ `_u^o `| $\underset{!}{=}$ `\underset{!}{=}` | $a+\left(\vcenter{\frac{\frac a b}c}\right)$ `a+\left(\vcenter{\hbox{$\frac{\frac a b}c$}}\right)`
||| $$\sum_{\substack{0<i<m\\0<j<n}}$$ `\sum_{\substack{0<i<m\\0<j<n}}`

`\raisebox` and `\hbox` put their argument into text mode. To raise math, nest `$…$` delimiters inside the argument as shown above. 

`\vcenter` can be written without an `\hbox` if the `strict` rendering option is *false*. In that case, omit the nested `$…$` delimiters.

### Overlap and Spacing

|||
|:-------|:-------|
|${=}\mathllap{/\,}$ `{=}\mathllap{/\,}` | $\left(x^{\smash{2}}\right)$ `\left(x^{\smash{2}}\right)`
|$\mathrlap{\,/}{=}$ `\mathrlap{\,/}{=}` | $\sqrt{\smash[b]{y}}$ `\sqrt{\smash[b]{y}} `

$\displaystyle\sum_{\mathclap{1\le i\le j\le n}} x_{ij}$ `\sum_{\mathclap{1\le i\le j\le n}} x_{ij}`

KaTeX also supports `\llap`, `\rlap`, and `\clap`, but they will take only text, not math, as arguments.

</div>
<div class="katex-cards" id="spacing-tbl">

**Spacing**

| Function        | Produces           | Function             | Produces|
|:----------------|:-------------------|:---------------------|:--------------------------------------|
| `\,`            | ³∕₁₈ em space      | `\kern{distance}`    | space, width = *distance*
| `\thinspace`    | ³∕₁₈ em space      | `\mkern{distance}`   | space, width = *distance*
| `\>`            | ⁴∕₁₈ em space      | `\mskip{distance}`   | space, width = *distance*
| `\:`            | ⁴∕₁₈ em space      | `\hskip{distance}`   | space, width = *distance*
| `\medspace`     | ⁴∕₁₈ em space      | `\hspace{distance}`  | space, width = *distance*
| `\;`            | ⁵∕₁₈ em space      | `\hspace*{distance}` | space, width = *distance*
| `\thickspace`   | ⁵∕₁₈ em space      | `\phantom{content}`  | space the width and height of content
| `\enspace`      | ½ em space         | `\hphantom{content}` | space the width of content
| `\quad`         | 1 em space         | `\vphantom{content}` | a strut the height of content
| `\qquad`        | 2 em space         | `\!`                 | – ³∕₁₈ em space
| `~`             | non-breaking space | `\negthinspace`      | – ³∕₁₈ em space
| `\<space>`      | space              | `\negmedspace`       | – ⁴∕₁₈ em space
| `\nobreakspace` | non-breaking space | `\negthickspace`     | – ⁵∕₁₈ em space
| `\space`        | space              | `\mathstrut`         | `\vphantom{(}`

</div>

**Notes:**

`distance` will accept any of the [KaTeX units](#units).

`\kern`, `\mkern`, `\mskip`, and `\hspace` accept unbraced distances, as in: `\kern1em`.

`\mkern` and `\mskip` will not work in text mode and both will write a console warning for any unit except `mu`.

<div class="katex-hopscotch">

## Logic and Set Theory

$\gdef\VERT{|}$

|||||
|:--------------------|:--------------------------|:----------------------------|:-----
|$\forall$ `\forall`  |$\complement$ `\complement`|$\therefore$ `\therefore`    |$\emptyset$ `\emptyset`
|$\exists$ `\exists`  |$\subset$ `\subset`  |$\because$ `\because`              |$\empty$ `\empty`
|$\exist$ `\exist`    |$\supset$ `\supset`  |$\mapsto$ `\mapsto`                |$\varnothing$ `\varnothing`
|$\nexists$ `\nexists`|$\mid$ `\mid`        |$\to$ `\to`                        |$\implies$ `\implies`
|$\in$ `\in`          |$\land$ `\land`      |$\gets$ `\gets`                    |$\impliedby$ `\impliedby`
|$\isin$ `\isin`      |$\lor$ `\lor`        |$\leftrightarrow$ `\leftrightarrow`|$\iff$ `\iff`
|$\notin$ `\notin`    |$\ni$ `\ni`          |$\notni$ `\notni`                  |$\neg$ `\neg` or `\lnot`
|   | $\Set{ x \VERT x<\frac 1 2 }$<br><code>\Set{ x &#124; x<\frac 1 2 }</code>  | $\set{x\VERT x<5}$<br><code>\set{x&#124;x<5}</code> ||

Direct Input: $∀ ∴ ∁ ∵ ∃ ∣ ∈ ∉ ∋ ⊂ ⊃ ∧ ∨ ↦ → ← ↔ ¬$ ℂ ℍ ℕ ℙ ℚ ℝ

## Macros

|||
|:-------------------------------------|:------
|$\def\foo{x^2} \foo + \foo$           | `\def\foo{x^2} \foo + \foo`
|$\gdef\foo#1{#1^2} \foo{y} + \foo{y}$ | `\gdef\foo#1{#1^2} \foo{y} + \foo{y}`
|                                      | `\edef\macroname#1#2…{definition to be expanded}`
|                                      | `\xdef\macroname#1#2…{definition to be expanded}`
|                                      | `\let\foo=\bar`
|                                      | `\futurelet\foo\bar x`
|                                      | `\global\def\macroname#1#2…{definition}`
|                                      | `\newcommand\macroname[numargs]{definition}`
|                                      | `\renewcommand\macroname[numargs]{definition}`
|                                      | `\providecommand\macroname[numargs]{definition}`

Macros can also be defined in the KaTeX [rendering options](options.md).

Macros accept up to nine arguments: #1, #2, etc.

</div>

<div id="gdef">

Macros defined by `\gdef`, `\xdef`, `\global\def`, `\global\edef`, `\global\let`, and `\global\futurelet` will persist between math expressions. (Exception: macro persistence may be disabled. There are legitimate security reasons for that.)

KaTeX has no `\par`, so all macros are long by default and `\long` will be ignored.

Available functions include:

`\char` `\mathchoice` `\TextOrMath` `\@ifstar` `\@ifnextchar` `\@firstoftwo` `\@secondoftwo` `\relax` `\expandafter` `\noexpand`

@ is a valid character for commands, as if `\makeatletter` were in effect.

## Operators

### Big Operators

|||||
|------------------|-------------------------|--------------------------|--------------|
| $\sum$ `\sum`    | $\prod$ `\prod`         | $\bigotimes$ `\bigotimes`| $\bigvee$ `\bigvee`
| $\int$ `\int`    | $\coprod$ `\coprod`     | $\bigoplus$ `\bigoplus`  | $\bigwedge$ `\bigwedge`
| $\iint$ `\iint`  | $\intop$ `\intop`       | $\bigodot$ `\bigodot`    | $\bigcap$ `\bigcap`
| $\iiint$ `\iiint`| $\smallint$ `\smallint` | $\biguplus$ `\biguplus`  | $\bigcup$ `\bigcup`
| $\oint$ `\oint`  | $\oiint$ `\oiint`       | $\oiiint$ `\oiiint`      | $\bigsqcup$ `\bigsqcup`

Direct Input: $∫ ∬ ∭ ∮ ∏ ∐ ∑ ⋀ ⋁ ⋂ ⋃ ⨀ ⨁ ⨂ ⨄ ⨆$ ∯ ∰

### Binary Operators

|||||
|-------------|-------------------|-------------------|--------------------|
| $+$ `+`| $\cdot$ `\cdot`  | $\gtrdot$ `\gtrdot`| $x \pmod a$ `x \pmod a`|
| $-$ `-`| $\cdotp$ `\cdotp` | $\intercal$ `\intercal` | $x \pod a$ `x \pod a` |
| $/$ `/`| $\centerdot$ `\centerdot`| $\land$ `\land`  | $\rhd$ `\rhd` |
| $*$ `*`| $\circ$ `\circ`  | $\leftthreetimes$ `\leftthreetimes` | $\rightthreetimes$ `\rightthreetimes` |
| $\amalg$ `\amalg` | $\circledast$ `\circledast`  | $\ldotp$ `\ldotp` | $\rtimes$ `\rtimes` |
| $\And$ `\And`| $\circledcirc$ `\circledcirc` | $\lor$ `\lor`| $\setminus$ `\setminus`  |
| $\ast$ `\ast`| $\circleddash$ `\circleddash` | $\lessdot$ `\lessdot`  | $\smallsetminus$ `\smallsetminus`|
| $\barwedge$ `\barwedge` | $\Cup$ `\Cup`| $\lhd$ `\lhd`| $\sqcap$ `\sqcap`  |
| $\bigcirc$ `\bigcirc`  | $\cup$ `\cup`| $\ltimes$ `\ltimes`| $\sqcup$ `\sqcup`  |
| $\bmod$ `\bmod`  | $\curlyvee$ `\curlyvee` | $x \mod a$ `x\mod a`| $\times$ `\times`  |
| $\boxdot$ `\boxdot`| $\curlywedge$ `\curlywedge`  | $\mp$ `\mp` | $\unlhd$ `\unlhd`  |
| $\boxminus$ `\boxminus` | $\div$ `\div`| $\odot$ `\odot`  | $\unrhd$ `\unrhd`  |
| $\boxplus$ `\boxplus`  | $\divideontimes$ `\divideontimes`  | $\ominus$ `\ominus`| $\uplus$ `\uplus`  |
| $\boxtimes$ `\boxtimes` | $\dotplus$ `\dotplus`  | $\oplus$ `\oplus` | $\vee$ `\vee` |
| $\bullet$ `\bullet`| $\doublebarwedge$ `\doublebarwedge` | $\otimes$ `\otimes`| $\veebar$ `\veebar` |
| $\Cap$ `\Cap`| $\doublecap$ `\doublecap`| $\oslash$ `\oslash`| $\wedge$ `\wedge`  |
| $\cap$ `\cap`| $\doublecup$ `\doublecup`| $\pm$ `\pm` or `\plusmn` | $\wr$ `\wr`  |

Direct Input: $+ - / * ⋅ ∘ ∙ ± × ÷ ∓ ∔ ∧ ∨ ∩ ∪ ≀ ⊎ ⊓ ⊔ ⊕ ⊖ ⊗ ⊘ ⊙ ⊚ ⊛ ⊝ ◯ ∖ {}$

### Fractions and Binomials

||||
|:--------------------------|:----------------------------|:-----
|$\frac{a}{b}$ `\frac{a}{b}`|$\tfrac{a}{b}$ `\tfrac{a}{b}`|$\genfrac ( ] {2pt}{1}a{a+1}$ `\genfrac ( ] {2pt}{1}a{a+1}`
|${a \over b}$ `{a \over b}`|$\dfrac{a}{b}$ `\dfrac{a}{b}`|${a \above{2pt} b+1}$ `{a \above{2pt} b+1}`
|$a/b$ `a/b`                |  |$\cfrac{a}{1 + \cfrac{1}{b}}$ `\cfrac{a}{1 + \cfrac{1}{b}}`

||||
|:------------------------------|:------------------------------|:--------
|$\binom{n}{k}$ `\binom{n}{k}`  |$\dbinom{n}{k}$ `\dbinom{n}{k}`|${n\brace k}$ `{n\brace k}`
|${n \choose k}$ `{n \choose k}`|$\tbinom{n}{k}$ `\tbinom{n}{k}`|${n\brack k}$ `{n\brack k}`

### Math Operators

|||||
|:--------------------|:--------------------|:----------------|:--------------|
| $\arcsin$ `\arcsin` | $\cosec$ `\cosec`   | $\deg$ `\deg`   | $\sec$ `\sec` |
| $\arccos$ `\arccos` | $\cosh$ `\cosh`     | $\dim$ `\dim`   | $\sin$ `\sin` |
| $\arctan$ `\arctan` | $\cot$ `\cot`       | $\exp$ `\exp`   | $\sinh$ `\sinh` |
| $\arctg$ `\arctg`   | $\cotg$ `\cotg`     | $\hom$ `\hom`   | $\sh$ `\sh` |
| $\arcctg$ `\arcctg` | $\coth$ `\coth`     | $\ker$ `\ker`   | $\tan$ `\tan` |
| $\arg$ `\arg`       | $\csc$ `\csc`       | $\lg$ `\lg`     | $\tanh$ `\tanh` |
| $\ch$ `\ch`         | $\ctg$ `\ctg`       | $\ln$ `\ln`     | $\tg$ `\tg` |
| $\cos$ `\cos`       | $\cth$ `\cth`       | $\log$ `\log`   | $\th$ `\th` |
| $\operatorname{f}$ `\operatorname{f}`     | |||
| $\argmax$ `\argmax` | $\injlim$ `\injlim` | $\min$ `\min`   | $\varinjlim$ `\varinjlim` |
| $\argmin$ `\argmin` | $\lim$ `\lim`       | $\plim$ `\plim` | $\varliminf$ `\varliminf` |
| $\det$ `\det`       | $\liminf$ `\liminf` | $\Pr$ `\Pr`     | $\varlimsup$ `\varlimsup` |
| $\gcd$ `\gcd`       | $\limsup$ `\limsup` | $\projlim$ `\projlim` | $\varprojlim$ `\varprojlim` |
| $\inf$ `\inf`       | $\max$ `\max`       | $\sup$ `\sup`   ||
| $\operatorname*{f}$ `\operatorname*{f}` | $\operatornamewithlimits{f}$ `\operatornamewithlimits{f}` |||

Functions in the bottom six rows of this table can take `\limits`.

### \sqrt

$\sqrt{x}$ `\sqrt{x}`

$\sqrt[3]{x}$ `\sqrt[3]{x}`

## Relations

$\stackrel{!}{=}$ `\stackrel{!}{=}`

|||||
|:--------|:------------------------|:----------------------------|:------------------|
| $=$ `=` | $\doteqdot$ `\doteqdot` | $\lessapprox$ `\lessapprox` | $\smile$ `\smile` |
| $<$ `<` | $\eqcirc$ `\eqcirc` | $\lesseqgtr$ `\lesseqgtr` | $\sqsubset$ `\sqsubset` |
| $>$ `>` | $\eqcolon$ `\eqcolon` or<br>    `\minuscolon` | $\lesseqqgtr$ `\lesseqqgtr` | $\sqsubseteq$ `\sqsubseteq` |
| $:$ `:` | $\Eqcolon$ `\Eqcolon` or<br>    `\minuscoloncolon` | $\lessgtr$ `\lessgtr` | $\sqsupset$ `\sqsupset` |
| $\approx$ `\approx` | $\eqqcolon$ `\eqqcolon` or<br>    `\equalscolon` | $\lesssim$ `\lesssim` | $\sqsupseteq$ `\sqsupseteq` |
| $\approxcolon$ `\approxcolon` | $\Eqqcolon$ `\Eqqcolon` or<br>    `\equalscoloncolon` | $\ll$ `\ll` | $\Subset$ `\Subset` |
| $\approxcoloncolon$ `\approxcoloncolon` | $\eqsim$ `\eqsim` | $\lll$ `\lll` | $\subset$ `\subset` or `\sub` |
| $\approxeq$ `\approxeq` | $\eqslantgtr$ `\eqslantgtr` | $\llless$ `\llless` | $\subseteq$ `\subseteq` or `\sube` |
| $\asymp$ `\asymp` | $\eqslantless$ `\eqslantless` | $\lt$ `\lt` | $\subseteqq$ `\subseteqq` |
| $\backepsilon$ `\backepsilon` | $\equiv$ `\equiv` | $\mid$ `\mid` | $\succ$ `\succ` |
| $\backsim$ `\backsim` | $\fallingdotseq$ `\fallingdotseq` | $\models$ `\models` | $\succapprox$ `\succapprox` |
| $\backsimeq$ `\backsimeq` | $\frown$ `\frown` | $\multimap$ `\multimap` | $\succcurlyeq$ `\succcurlyeq` |
| $\between$ `\between` | $\ge$ `\ge` | $\origof$ `\origof` | $\succeq$ `\succeq` |
| $\bowtie$ `\bowtie` | $\geq$ `\geq` | $\owns$ `\owns` | $\succsim$ `\succsim` |
| $\bumpeq$ `\bumpeq` | $\geqq$ `\geqq` | $\parallel$ `\parallel` | $\Supset$ `\Supset` |
| $\Bumpeq$ `\Bumpeq` | $\geqslant$ `\geqslant` | $\perp$ `\perp` | $\supset$ `\supset` |
| $\circeq$ `\circeq` | $\gg$ `\gg` | $\pitchfork$ `\pitchfork` | $\supseteq$ `\supseteq` or `\supe` |
| $\colonapprox$ `\colonapprox` | $\ggg$ `\ggg` | $\prec$ `\prec` | $\supseteqq$ `\supseteqq` |
| $\Colonapprox$ `\Colonapprox` or<br>    `\coloncolonapprox` | $\gggtr$ `\gggtr` | $\precapprox$ `\precapprox` | $\thickapprox$ `\thickapprox` |
| $\coloneq$ `\coloneq` or<br>    `\colonminus` | $\gt$ `\gt` | $\preccurlyeq$ `\preccurlyeq` | $\thicksim$ `\thicksim` |
| $\Coloneq$ `\Coloneq` or<br>    `\coloncolonminus` | $\gtrapprox$ `\gtrapprox` | $\preceq$ `\preceq` | $\trianglelefteq$ `\trianglelefteq` |
| $\coloneqq$ `\coloneqq` or<br>   `\colonequals` | $\gtreqless$ `\gtreqless` | $\precsim$ `\precsim` | $\triangleq$ `\triangleq` |
| $\Coloneqq$ `\Coloneqq` or<br>    `\coloncolonequals` | $\gtreqqless$ `\gtreqqless` | $\propto$ `\propto` | $\trianglerighteq$ `\trianglerighteq` |
| $\colonsim$ `\colonsim` | $\gtrless$ `\gtrless` | $\risingdotseq$ `\risingdotseq` | $\varpropto$ `\varpropto` |
| $\Colonsim$ `\Colonsim` or<br>    `\coloncolonsim` | $\gtrsim$ `\gtrsim` | $\shortmid$ `\shortmid` | $\vartriangle$ `\vartriangle` |
| $\cong$ `\cong` | $\imageof$ `\imageof` | $\shortparallel$ `\shortparallel` | $\vartriangleleft$ `\vartriangleleft` |
| $\curlyeqprec$ `\curlyeqprec` | $\in$ `\in` or `\isin` | $\sim$ `\sim` | $\vartriangleright$ `\vartriangleright` |
| $\curlyeqsucc$ `\curlyeqsucc` | $\Join$ `\Join` | $\simcolon$ `\simcolon` | $\vcentcolon$ `\vcentcolon` or<br>   `\ratio` |
| $\dashv$ `\dashv` | $\le$ `\le` | $\simcoloncolon$ `\simcoloncolon` | $\vdash$ `\vdash` |
| $\dblcolon$ `\dblcolon` or<br>   `\coloncolon` | $\leq$ `\leq` | $\simeq$ `\simeq` | $\vDash$ `\vDash` |
| $\doteq$ `\doteq` | $\leqq$ `\leqq` | $\smallfrown$ `\smallfrown` | $\Vdash$ `\Vdash` |
| $\Doteq$ `\Doteq` | $\leqslant$ `\leqslant` | $\smallsmile$ `\smallsmile` | $\Vvdash$ `\Vvdash` |

Direct Input: $= < > : ∈ ∋ ∝ ∼ ∽ ≂ ≃ ≅ ≈ ≊ ≍ ≎ ≏ ≐ ≑ ≒ ≓ ≖ ≗ ≜ ≡ ≤ ≥ ≦ ≧ ≫ ≬ ≳ ≷ ≺ ≻ ≼ ≽ ≾ ≿ ⊂ ⊃ ⊆ ⊇ ⊏ ⊐ ⊑ ⊒ ⊢ ⊣ ⊩ ⊪ ⊸ ⋈ ⋍ ⋐ ⋑ ⋔ ⋙ ⋛ ⋞ ⋟ ⌢ ⌣ ⩾ ⪆ ⪌ ⪕ ⪖ ⪯ ⪰ ⪷ ⪸ ⫅ ⫆ ≲ ⩽ ⪅ ≶ ⋚ ⪋ ⟂ ⊨ ⊶ ⊷$ `≔ ≕ ⩴`

### Negated Relations

$\not =$ `\not =`

|||||
|--------------|-------------------|---------------------|------------------|
| $\gnapprox$ `\gnapprox`  | $\ngeqslant$ `\ngeqslant`| $\nsubseteq$ `\nsubseteq`  | $\precneqq$ `\precneqq`|
| $\gneq$ `\gneq`| $\ngtr$ `\ngtr`  | $\nsubseteqq$ `\nsubseteqq` | $\precnsim$ `\precnsim`|
| $\gneqq$ `\gneqq`  | $\nleq$ `\nleq`  | $\nsucc$ `\nsucc`| $\subsetneq$ `\subsetneq`  |
| $\gnsim$ `\gnsim`  | $\nleqq$ `\nleqq` | $\nsucceq$ `\nsucceq` | $\subsetneqq$ `\subsetneqq` |
| $\gvertneqq$ `\gvertneqq` | $\nleqslant$ `\nleqslant`| $\nsupseteq$ `\nsupseteq`  | $\succnapprox$ `\succnapprox`|
| $\lnapprox$ `\lnapprox`  | $\nless$ `\nless` | $\nsupseteqq$ `\nsupseteqq` | $\succneqq$ `\succneqq`|
| $\lneq$ `\lneq`| $\nmid$ `\nmid`  | $\ntriangleleft$ `\ntriangleleft` | $\succnsim$ `\succnsim`|
| $\lneqq$ `\lneqq`  | $\notin$ `\notin` | $\ntrianglelefteq$ `\ntrianglelefteq`  | $\supsetneq$ `\supsetneq`  |
| $\lnsim$ `\lnsim`  | $\notni$ `\notni` | $\ntriangleright$ `\ntriangleright`| $\supsetneqq$ `\supsetneqq` |
| $\lvertneqq$ `\lvertneqq` | $\nparallel$ `\nparallel`| $\ntrianglerighteq$ `\ntrianglerighteq` | $\varsubsetneq$ `\varsubsetneq`  |
| $\ncong$ `\ncong`  | $\nprec$ `\nprec` | $\nvdash$ `\nvdash`  | $\varsubsetneqq$ `\varsubsetneqq` |
| $\ne$ `\ne`  | $\npreceq$ `\npreceq`  | $\nvDash$ `\nvDash`  | $\varsupsetneq$ `\varsupsetneq`  |
| $\neq$ `\neq` | $\nshortmid$ `\nshortmid`| $\nVDash$ `\nVDash`  | $\varsupsetneqq$ `\varsupsetneqq` |
| $\ngeq$ `\ngeq`| $\nshortparallel$ `\nshortparallel` | $\nVdash$ `\nVdash`  |
| $\ngeqq$ `\ngeqq`  | $\nsim$ `\nsim`  | $\precnapprox$ `\precnapprox`|

Direct Input: $∉ ∌ ∤ ∦ ≁ ≆ ≠ ≨ ≩ ≮ ≯ ≰ ≱ ⊀ ⊁ ⊈ ⊉ ⊊ ⊋ ⊬ ⊭ ⊮ ⊯ ⋠ ⋡ ⋦ ⋧ ⋨ ⋩ ⋬ ⋭ ⪇ ⪈ ⪉ ⪊ ⪵ ⪶ ⪹ ⪺ ⫋ ⫌$

### Arrows

||||
|:----------|:----------|:----------|
|$\circlearrowleft$ `\circlearrowleft`|$\leftharpoonup$ `\leftharpoonup`|$\rArr$ `\rArr`
|$\circlearrowright$ `\circlearrowright`|$\leftleftarrows$ `\leftleftarrows`|$\rarr$ `\rarr`
|$\curvearrowleft$ `\curvearrowleft`|$\leftrightarrow$ `\leftrightarrow`|$\restriction$ `\restriction`
|$\curvearrowright$ `\curvearrowright`|$\Leftrightarrow$ `\Leftrightarrow`|$\rightarrow$ `\rightarrow`
|$\Darr$ `\Darr`|$\leftrightarrows$ `\leftrightarrows`|$\Rightarrow$ `\Rightarrow`
|$\dArr$ `\dArr`|$\leftrightharpoons$ `\leftrightharpoons`|$\rightarrowtail$ `\rightarrowtail`
|$\darr$ `\darr`|$\leftrightsquigarrow$ `\leftrightsquigarrow`|$\rightharpoondown$ `\rightharpoondown`
|$\dashleftarrow$ `\dashleftarrow`|$\Lleftarrow$ `\Lleftarrow`|$\rightharpoonup$ `\rightharpoonup`
|$\dashrightarrow$ `\dashrightarrow`|$\longleftarrow$ `\longleftarrow`|$\rightleftarrows$ `\rightleftarrows`
|$\downarrow$ `\downarrow`|$\Longleftarrow$ `\Longleftarrow`|$\rightleftharpoons$ `\rightleftharpoons`
|$\Downarrow$ `\Downarrow`|$\longleftrightarrow$ `\longleftrightarrow`|$\rightrightarrows$ `\rightrightarrows`
|$\downdownarrows$ `\downdownarrows`|$\Longleftrightarrow$ `\Longleftrightarrow`|$\rightsquigarrow$ `\rightsquigarrow`
|$\downharpoonleft$ `\downharpoonleft`|$\longmapsto$ `\longmapsto`|$\Rrightarrow$ `\Rrightarrow`
|$\downharpoonright$ `\downharpoonright`|$\longrightarrow$ `\longrightarrow`|$\Rsh$ `\Rsh`
|$\gets$ `\gets`|$\Longrightarrow$ `\Longrightarrow`|$\searrow$ `\searrow`
|$\Harr$ `\Harr`|$\looparrowleft$ `\looparrowleft`|$\swarrow$ `\swarrow`
|$\hArr$ `\hArr`|$\looparrowright$ `\looparrowright`|$\to$ `\to`
|$\harr$ `\harr`|$\Lrarr$ `\Lrarr`|$\twoheadleftarrow$ `\twoheadleftarrow`
|$\hookleftarrow$ `\hookleftarrow`|$\lrArr$ `\lrArr`|$\twoheadrightarrow$ `\twoheadrightarrow`
|$\hookrightarrow$ `\hookrightarrow`|$\lrarr$ `\lrarr`|$\Uarr$ `\Uarr`
|$\iff$ `\iff`|$\Lsh$ `\Lsh`|$\uArr$ `\uArr`
|$\impliedby$ `\impliedby`|$\mapsto$ `\mapsto`|$\uarr$ `\uarr`
|$\implies$ `\implies`|$\nearrow$ `\nearrow`|$\uparrow$ `\uparrow`
|$\Larr$ `\Larr`|$\nleftarrow$ `\nleftarrow`|$\Uparrow$ `\Uparrow`
|$\lArr$ `\lArr`|$\nLeftarrow$ `\nLeftarrow`|$\updownarrow$ `\updownarrow`
|$\larr$ `\larr`|$\nleftrightarrow$ `\nleftrightarrow`|$\Updownarrow$ `\Updownarrow`
|$\leadsto$ `\leadsto`|$\nLeftrightarrow$ `\nLeftrightarrow`|$\upharpoonleft$ `\upharpoonleft`
|$\leftarrow$ `\leftarrow`|$\nrightarrow$ `\nrightarrow`|$\upharpoonright$ `\upharpoonright`
|$\Leftarrow$ `\Leftarrow`|$\nRightarrow$ `\nRightarrow`|$\upuparrows$ `\upuparrows`
|$\leftarrowtail$ `\leftarrowtail`|$\nwarrow$ `\nwarrow`
|$\leftharpoondown$ `\leftharpoondown`|$\Rarr$ `\Rarr`

Direct Input: $← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↚ ↛ ↞ ↠ ↢ ↣ ↦ ↩ ↪ ↫ ↬ ↭ ↮ ↰ ↱↶ ↷ ↺ ↻ ↼ ↽ ↾ ↾ ↿ ⇀ ⇁ ⇂ ⇃ ⇄ ⇆ ⇇ ⇈ ⇉ ⇊ ⇋ ⇌⇍ ⇎ ⇏ ⇐ ⇑ ⇒ ⇓ ⇔ ⇕ ⇚ ⇛ ⇝ ⇠ ⇢ ⟵ ⟶ ⟷ ⟸ ⟹ ⟺ ⟼$ ↽

**Extensible Arrows**

|||
|:----------------------------------------------------|:-----
|$\xleftarrow{abc}$ `\xleftarrow{abc}`                |$\xrightarrow[under]{over}$ `\xrightarrow[under]{over}`
|$\xLeftarrow{abc}$ `\xLeftarrow{abc}`                |$\xRightarrow{abc}$ `\xRightarrow{abc}`
|$\xleftrightarrow{abc}$ `\xleftrightarrow{abc}`      |$\xLeftrightarrow{abc}$ `\xLeftrightarrow{abc}`
|$\xhookleftarrow{abc}$ `\xhookleftarrow{abc}`        |$\xhookrightarrow{abc}$ `\xhookrightarrow{abc}`
|$\xtwoheadleftarrow{abc}$ `\xtwoheadleftarrow{abc}`  |$\xtwoheadrightarrow{abc}$ `\xtwoheadrightarrow{abc}`
|$\xleftharpoonup{abc}$ `\xleftharpoonup{abc}`        |$\xrightharpoonup{abc}$ `\xrightharpoonup{abc}`
|$\xleftharpoondown{abc}$ `\xleftharpoondown{abc}`    |$\xrightharpoondown{abc}$ `\xrightharpoondown{abc}`
|$\xleftrightharpoons{abc}$ `\xleftrightharpoons{abc}`|$\xrightleftharpoons{abc}$ `\xrightleftharpoons{abc}`
|$\xtofrom{abc}$ `\xtofrom{abc}`                      |$\xmapsto{abc}$ `\xmapsto{abc}`
|$\xlongequal{abc}$ `\xlongequal{abc}`

Extensible arrows all can take an optional argument in the same manner<br>as `\xrightarrow[under]{over}`.

## Special Notation

**Bra-ket Notation**

||||
|:----------|:----------|:----------|
|$\bra{\phi}$ `\bra{\phi}` |$\ket{\psi}$ `\ket{\psi}` |$\braket{\phi\VERT\psi}$ <code>\braket{\phi&#124;\psi}</code> |
|$\Bra{\phi}$ `\Bra{\phi}` |$\Ket{\psi}$ `\Ket{\psi}` |$\Braket{ ϕ \VERT \frac{∂^2}{∂ t^2} \VERT ψ }$ <code>\Braket{ ϕ &#124; \frac{∂^2}{∂ t^2} &#124; ψ }</code>|

## Style, Color, Size, and Font

**Class Assignment**

`\mathbin` `\mathclose` `\mathinner` `\mathop`<br>
`\mathopen` `\mathord` `\mathpunct` `\mathrel`

**Color**

$\color{blue} F=ma$  `\color{blue} F=ma`

Note that `\color` acts like a switch. Other color functions expect the content to be a function argument:

$\textcolor{blue}{F=ma}$ `\textcolor{blue}{F=ma}`<br>
$\textcolor{#228B22}{F=ma}$ `\textcolor{#228B22}{F=ma}`<br>
$\colorbox{aqua}{$F=ma$}$ `\colorbox{aqua}{$F=ma$}`<br>
$\fcolorbox{red}{aqua}{$F=ma$}$ `\fcolorbox{red}{aqua}{$F=ma$}`

Note that, as in LaTeX, `\colorbox` & `\fcolorbox` renders its third argument as text, so you may want to switch back to math mode with `$` as in the examples above.

For color definition, KaTeX color functions will accept the standard HTML [predefined color names](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#Color_keywords). They will also accept an RGB argument in CSS hexa­decimal style. The "#" is optional before a six-digit specification.

**Font**

||||
|:------------------------------------|:------------------------------------|:--------------------------------|
|$\mathrm{Ab0}$ `\mathrm{Ab0}`        |$\mathbf{Ab0}$ `\mathbf{Ab0}`        |$\mathsf{Ab0}$ `\mathsf{Ab0}`    |
|$\mathnormal{Ab0}$ `\mathnormal{Ab0}`|$\textbf{Ab0}$ `\textbf{Ab0}`        |$\textsf{Ab0}$ `\textsf{Ab0}`    |
|$\textrm{Ab0}$ `\textrm{Ab0}`        |$\bf Ab0$ `\bf Ab0`                  |$\sf Ab0$ `\sf Ab0`              |
|$\rm Ab0$ `\rm Ab0`                  |$\bold{Ab0}$ `\bold{Ab0}`            |$\mathsfit{Ab0}$ `\mathsfit{Ab0}`|
|$\textnormal{Ab0}$ `\textnormal{Ab0}`|$\boldsymbol{Ab0}$ `\boldsymbol{Ab0}`|$\Bbb{AB}$ `\Bbb{AB}`            |
|$\text{Ab0}$ `\text{Ab0}`            |$\bm{Ab0}$ `\bm{Ab0}`                |$\mathbb{AB}$ `\mathbb{AB}`      |
|$\textup{Ab0}$ `\textup{Ab0}`        |$\textmd{Ab0}$ `\textmd{Ab0}`        |$\frak{Ab0}$ `\frak{Ab0}`        |
|$\mathit{Ab0}$ `\mathit{Ab0}`        |$\mathtt{Ab0}$ `\mathtt{Ab0}`        |$\mathfrak{Ab0}$ `\mathfrak{Ab0}`|
|$\textit{Ab0}$ `\textit{Ab0}`        |$\texttt{Ab0}$ `\texttt{Ab0}`        |$\mathcal{AB0}$ `\mathcal{AB0}`  |
|$\it Ab0$ `\it Ab0`                  |$\tt Ab0$ `\tt Ab0`                  |$\cal AB0$ `\cal AB0`            |
|$\emph{Ab0}$ `\emph{Ab0}`            |                                     |$\mathscr{AB}$ `\mathscr{AB}`    |

One can stack font family, font weight, and font shape by using the `\textXX` versions of the font functions. So `\textsf{\textbf{H}}` will produce $\textsf{\textbf{H}}$. The other versions do not stack, e.g., `\mathsf{\mathbf{H}}` will produce $\mathsf{\mathbf{H}}$.

In cases where KaTeX fonts do not have a bold glyph, `\pmb` can simulate one. For example, `\pmb{\mu}` renders as : $\pmb{\mu}$

**Size**

|||
|:----------------------|:-----
|$\Huge AB$ `\Huge AB`  |$\normalsize AB$ `\normalsize AB`
|$\huge AB$ `\huge AB`  |$\small AB$ `\small AB`
|$\LARGE AB$ `\LARGE AB`|$\footnotesize AB$ `\footnotesize AB`
|$\Large AB$ `\Large AB`|$\scriptsize AB$ `\scriptsize AB`
|$\large AB$ `\large AB`|$\tiny AB$ `\tiny AB`


**Style**

||
|:-------------------------------------------------------|
|$\displaystyle\sum_{i=1}^n$ `\displaystyle\sum_{i=1}^n`
|$\textstyle\sum_{i=1}^n$ `\textstyle\sum_{i=1}^n`
|$\scriptstyle x$ `\scriptstyle x` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(The size of a first sub/superscript)
|$\scriptscriptstyle x$ `\scriptscriptstyle x` (The size of subsequent sub/superscripts)
|$\lim\limits_x$ `\lim\limits_x`
|$\lim\nolimits_x$ `\lim\nolimits_x`
|$\verb!x^2!$ `\verb!x^2!`

`\text{…}` will accept nested `$…$` fragments and render them in math mode.

## Symbols and Punctuation

||||
|:----------|:----------|:----------|
|`% comment`|$\dots$ `\dots`|$\KaTeX$ `\KaTeX`
|$\%$ `\%`|$\cdots$ `\cdots`|$\LaTeX$ `\LaTeX`
|$\#$ `\#`|$\ddots$ `\ddots`|$\TeX$ `\TeX`
|$\&$ `\&`|$\ldots$ `\ldots`|$\nabla$ `\nabla`
|$\_$ `\_`|$\vdots$ `\vdots`|$\infty$ `\infty`
|$\text{\textunderscore}$ `\text{\textunderscore}`|$\dotsb$ `\dotsb`|$\infin$ `\infin`
|$\text{--}$ `\text{--}`|$\dotsc$ `\dotsc`|$\checkmark$ `\checkmark`
|$\text{\textendash}$ `\text{\textendash}`|$\dotsi$ `\dotsi`|$\dag$ `\dag`
|$\text{---}$ `\text{---}`|$\dotsm$ `\dotsm`|$\dagger$ `\dagger`
|$\text{\textemdash}$ `\text{\textemdash}`|$\dotso$ `\dotso`|$\text{\textdagger}$ `\text{\textdagger}`
|$\text{\textasciitilde}$ `\text{\textasciitilde}`|$\sdot$ `\sdot`|$\ddag$ `\ddag`
|$\text{\textasciicircum}$ `\text{\textasciicircum}`|$\mathellipsis$ `\mathellipsis`|$\ddagger$ `\ddagger`
|$`$ <code>`</code>|$\text{\textellipsis}$ `\text{\textellipsis}`|$\text{\textdaggerdbl}$ `\text{\textdaggerdbl}`
|$\text{\textquoteleft}$ `text{\textquoteleft}`|$\Box$ `\Box`|$\Dagger$ `\Dagger`
|$\lq$ `\lq`|$\square$ `\square`|$\angle$ `\angle`
|$\text{\textquoteright}$ `\text{\textquoteright}`|$\blacksquare$ `\blacksquare`|$\measuredangle$ `\measuredangle`
|$\rq$ `\rq`|$\triangle$ `\triangle`|$\sphericalangle$ `\sphericalangle`
|$\text{\textquotedblleft}$ `\text{\textquotedblleft}`|$\triangledown$ `\triangledown`|$\top$ `\top`
|$"$ `"`|$\triangleleft$ `\triangleleft`|$\bot$ `\bot`
|$\text{\textquotedblright}$ `\text{\textquotedblright}`|$\triangleright$ `\triangleright`|$\$$ `\$`
|$\colon$ `\colon`|$\bigtriangledown$ `\bigtriangledown`|$\text{\textdollar}$ `\text{\textdollar}`
|$\backprime$ `\backprime`|$\bigtriangleup$ `\bigtriangleup`|$\pounds$ `\pounds`
|$\prime$ `\prime`|$\blacktriangle$ `\blacktriangle`|$\mathsterling$ `\mathsterling`
|$\text{\textless}$ `\text{\textless}`|$\blacktriangledown$ `\blacktriangledown`|$\text{\textsterling}$ `\text{\textsterling}`
|$\text{\textgreater}$ `\text{\textgreater}`|$\blacktriangleleft$ `\blacktriangleleft`|$\yen$ `\yen`
|$\text{\textbar}$ `\text{\textbar}`|$\blacktriangleright$ `\blacktriangleright`|$\surd$ `\surd`
|$\text{\textbardbl}$ `\text{\textbardbl}`|$\diamond$ `\diamond`|$\degree$ `\degree`
|$\text{\textbraceleft}$ `\text{\textbraceleft}`|$\Diamond$ `\Diamond`|$\text{\textdegree}$ `\text{\textdegree}`
|$\text{\textbraceright}$ `\text{\textbraceright}`|$\lozenge$ `\lozenge`|$\mho$ `\mho`
|$\text{\textbackslash}$ `\text{\textbackslash}`|$\blacklozenge$ `\blacklozenge`|$\diagdown$ `\diagdown`
|$\text{\P}$ `\text{\P}` or `\P`|$\star$ `\star`|$\diagup$ `\diagup`
|$\text{\S}$ `\text{\S}` or `\S`|$\bigstar$ `\bigstar`|$\flat$ `\flat`
|$\text{\sect}$ `\text{\sect}`|$\clubsuit$ `\clubsuit`|$\natural$ `\natural`
|$\copyright$ `\copyright`|$\clubs$ `\clubs`|$\sharp$ `\sharp`
|$\circledR$ `\circledR`|$\diamondsuit$ `\diamondsuit`|$\heartsuit$ `\heartsuit`
|$\text{\textregistered}$ `\text{\textregistered}`|$\diamonds$ `\diamonds`|$\hearts$ `\hearts`
|$\circledS$ `\circledS`|$\spadesuit$ `\spadesuit`|$\spades$ `\spades`
|$\text{\textcircled a}$ `\text{\textcircled a}`|$\maltese$ `\maltese`|$\minuso$ `\minuso`|

Direct Input: § ¶ $ £ ¥ ∇ ∞ · ∠ ∡ ∢ ♠ ♡ ♢ ♣ ♭ ♮ ♯ ✓ …  ⋮  ⋯  ⋱  !$ ‼ ⦵

## Units

In KaTeX, units are proportioned as they are in TeX.<br>
KaTeX units are different than CSS units.

</div>
<div class="katex-cards" id="unit-tbl">

|  KaTeX Unit | Value       | KaTeX Unit  | Value  |
|:---|:---------------------|:---|:----------------|
| em | CSS em               | bp | 1/72​ inch × F × G|
| ex | CSS ex               | pc | 12 KaTeX pt|
| mu | 1/18 CSS em          | dd | 1238/1157​ KaTeX pt  |
| pt | 1/72.27 inch × F × G | cc | 14856/1157 KaTeX pt |
| mm | 1 mm × F × G         | nd | 685/642 KaTeX pt |
| cm | 1 cm × F × G         | nc | 1370/107​ KaTeX pt|
| in | 1 inch × F × G       | sp | 1/65536 KaTeX pt |

</div>

where:

<div style="margin-left: 1.5em;">

F = (font size of surrounding HTML text)/(10 pt)

G = 1.21 by default, because KaTeX font-size is normally 1.21 × the surrounding font size. This value [can be overridden](font.md#font-size-and-lengths) by the CSS of an HTML page.

</div>

The effect of style and size:

<div class="katex-cards" id="unit-blocks">

|  Unit  |     textstyle     | scriptscript |  huge  |
|:------:|:-----------------:|:------------:|:------:|
|em or ex|$\rule{1em}{1em}$  |$\scriptscriptstyle\rule{1em}{1em}$  |$\huge\rule{1em}{1em}$
| mu     |$\rule{18mu}{18mu}$|$\scriptscriptstyle\rule{18mu}{18mu}$|$\huge\rule{18mu}{18mu}$
| others |$\rule{10pt}{10pt}$|$\scriptscriptstyle\rule{10pt}{10pt}$|$\huge\rule{10pt}{10pt}$

</div>

---
id: support_table
title: Support Table
---
This is a list of TeX functions, sorted alphabetically. This list includes functions that KaTeX supports and some that it doesn't support. There is a similar page, with functions [sorted by type](supported.md).

If you know the shape of a character, but not its name, [Detexify](https://detexify.kirelabs.org/classify.html) can help.

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.25/dist/katex.min.css" integrity="sha384-WcoG4HRXMzYzfCgiyfrySxx90XSl2rxY5mnVY5TwtWE6KLrArNKn0T/mOgNL0Mmi" crossorigin="anonymous">
<style>
table tr,
table td {
    vertical-align: middle;
}
</style>

## Symbols

$\gdef\VERT{|}$

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\!|$n!$|`n!`|
|\\\!|$a\!b$|`a\!b`|
|#|$\def\sqr#1{#1^2} \sqr{y}$|`\def\sqr#1{#1^2} \sqr{y}`|
|\\#|$\#$||
|%||`%this is a comment`|
|\\%|$\%$||
|&|$\begin{matrix} a & b\cr c & d \end{matrix}$|`\begin{matrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{matrix}`|
|\\&|$\&$||
|'|$'$||
|\\\'|$\text{\'{a}}$|`\text{\'{a}}`|
|(|$($||
|)|$)$||
|\\\(…\\\)|$\text{\(\frac a b\)}$|`\text{\(\frac a b\)}`|
|\\ |$a\ b$|`a\ b`|
|\\"|$\text{\"{a}}$|`\text{\"{a}}`|
|\\$|$\text{\textdollar}$||
|\\,|$a\,\,{b}$|`a\,\,{b}`|
|\\.|$\text{\.{a}}$|`\text{\.{a}}`|
|\\:|$a\:\:{b}$|`a\:\:{b}`|
|\\;|$a\;\;{b}$|a`\;\;{b}`|
|_|$x_i$|`x_i`|
|\\_|$\_$||
|\\\`|$\text{\`{a}}$|`\text{\'{a}}`|
|&#060;|$<$||
|\\=|$\text{\={a}}$|`\text{\={a}}`|
| >|$>$||
|\\>|$a\>\>{b}$|`a\>\>{b}`|
|\[|$[$||
|\]|$]$||
|{|${a}$|`{a}`|
|}|${a}$|`{a}`|
|\\{|$\{$||
|\\}|$\}$||
|&#124;|$\vert$||
|\\&#124;|$\Vert$||
|~|$\text{no~no~no~breaks}$|`\text{no~no~no~breaks}`|
|\\~|$\text{\~{a}}$|`\text{\~{a}}`|
|\\\\ |$\begin{matrix} a & b\\ c & d\end{matrix}$|`\begin{matrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{matrix}`|
|^|$x^i$|`x^i`|
|\\^|$\text{\^{a}}$|`\text{\^{a}}`|

## A

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\AA|$\text{\AA}$|`\text{\AA}`|
|\aa|$\text{\aa}$|`\text{\aa}`|
|\above|${a \above{2pt} b+1}$|`{a \above{2pt} b+1}`|
|\abovewithdelims|<span style="color:firebrick;">Not supported</span>||
|\acute|$\acute e$|`\acute e`|
|\AE|$\text{\AE}$|`\text{\AE}`|
|\ae|$\text{\ae}$|`\text{\ae}`|
|\alef|$\alef$||
|\alefsym|$\alefsym$||
|\aleph|$\aleph$||
|{align}|$$\begin{align}a&=b+c\\d+e&=f\end{align}$$|`\begin{align}`<br>&nbsp;&nbsp;&nbsp;`a&=b+c \\`<br>&nbsp;&nbsp;&nbsp;`d+e&=f`<br>`\end{align}`|
|{align\*}|$$\begin{align*}a&=b+c\\d+e&=f\end{align*}$$|`\begin{align*}`<br>&nbsp;&nbsp;&nbsp;`a&=b+c \\`<br>&nbsp;&nbsp;&nbsp;`d+e&=f`<br>`\end{align*}`|
|{aligned}|$\begin{aligned}a&=b+c\\d+e&=f\end{aligned}$|`\begin{aligned}`<br>&nbsp;&nbsp;&nbsp;`a&=b+c \\`<br>&nbsp;&nbsp;&nbsp;`d+e&=f`<br>`\end{aligned}`|
|{alignat}|$$\begin{alignat}{2}10&x+&3&y=2\\3&x+&13&y=4\end{alignat}$$|`\begin{alignat}{2}`<br>&nbsp;&nbsp;&nbsp;`10&x+ &3&y = 2 \\`<br>&nbsp;&nbsp;&nbsp;` 3&x+&13&y = 4`<br>`\end{alignat}`|
|{alignat\*}|$$\begin{alignat*}{2}10&x+&3&y=2\\3&x+&13&y=4\end{alignat*}$$|`\begin{alignat*}{2}`<br>&nbsp;&nbsp;&nbsp;`10&x+ &3&y = 2 \\`<br>&nbsp;&nbsp;&nbsp;` 3&x+&13&y = 4`<br>`\end{alignat*}`|
|{alignedat}|$\begin{alignedat}{2}10&x+&3&y=2\\3&x+&13&y=4\end{alignedat}$|`\begin{alignedat}{2}`<br>&nbsp;&nbsp;&nbsp;`10&x+ &3&y = 2 \\`<br>&nbsp;&nbsp;&nbsp;` 3&x+&13&y = 4`<br>`\end{alignedat}`|
|\allowbreak|||
|\Alpha|$\Alpha$||
|\alpha|$\alpha$||
|\amalg|$\amalg$||
|\And|$\And$||
|\and|<span style="color:firebrick;">Not supported</span>|[Deprecated](https://en.wikipedia.org/wiki/Help:Displaying_a_formula#Deprecated_syntax)|
|\ang|<span style="color:firebrick;">Not supported</span>|[Deprecated](https://en.wikipedia.org/wiki/Help:Displaying_a_formula#Deprecated_syntax)|
|\angl|$a_{\angl n}$||
|\angln|$a_\angln$||
|\angle|$\angle$||
|\approx|$\approx$||
|\approxeq|$\approxeq$||
|\approxcolon|$\approxcolon$||
|\approxcoloncolon|$\approxcoloncolon$||
|\arccos|$\arccos$||
|\arcctg|$\arcctg$||
|\arcsin|$\arcsin$||
|\arctan|$\arctan$||
|\arctg|$\arctg$||
|\arg|$\arg$||
|\argmax|$\argmax$||
|\argmin|$\argmin$||
|{array}|$\begin{array}{cc}a&b\\c&d\end{array}$ | `\begin{array}{cc}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{array}`|
|\array|<span style="color:firebrick;">Not supported</span>|see `{array}`|
|\arraystretch|$\def\arraystretch{1.5}\begin{array}{cc}a&b\\c&d\end{array}$|`\def\arraystretch{1.5}`<br>`\begin{array}{cc}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{array}`|
|\Arrowvert|<span style="color:firebrick;">Not supported</span>|see `\Vert`|
|\arrowvert|<span style="color:firebrick;">Not supported</span>|see `\vert`|
|\ast|$\ast$||
|\asymp|$\asymp$||
|\atop|${a \atop b}$|`{a \atop b}`|
|\atopwithdelims|<span style="color:firebrick;">Not supported</span>||

## B

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\backepsilon|$\backepsilon$||
|\backprime|$\backprime$||
|\backsim|$\backsim$||
|\backsimeq|$\backsimeq$||
|\backslash|$\backslash$||
|\bar|$\bar{y}$|`\bar{y}`|
|\barwedge|$\barwedge$||
|\Bbb|$\Bbb{ABC}$|`\Bbb{ABC}`<br>KaTeX supports A-Z & k|
|\Bbbk|$\Bbbk$||
|\bbox|<span style="color:firebrick;">Not supported</span>||
|\bcancel|$\bcancel{5}$|`\bcancel{5}`|
|\because|$\because$||
|\begin|$\begin{matrix} a & b\\ c & d\end{matrix}$|`\begin{matrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{matrix}`|
|\begingroup|$\begingroup a}$|`\begingroup a}`|
|\Beta|$\Beta$||
|\beta|$\beta$||
|\beth|$\beth$||
|\between|$\between$||
|\bf|$\bf AaBb12$|`\bf AaBb12`|
|\bfseries|<span style="color:firebrick;">Not supported</span>||
|\big|$\big(\big)$|`\big(\big)`|
|\Big|$\Big(\Big)$|`\Big(\Big)`|
|\bigcap|$\bigcap$||
|\bigcirc|$\bigcirc$||
|\bigcup|$\bigcup$||
|\bigg|$\bigg(\bigg)$|`\bigg(\bigg)`|
|\Bigg|$\Bigg(\Bigg)$|`\Bigg(\Bigg)`|
|\biggl|$\biggl($|`\biggl(`|
|\Biggl|$\Biggl($|`\Biggl(`|
|\biggm|$\biggm\vert$|`\biggm\vert`|
|\Biggm|$\Biggm\vert$|`\Biggm\vert`|
|\biggr|$\biggr)$|`\biggr)`|
|\Biggr|$\Biggr)$|`\Biggr)`|
|\bigl|$\bigl($|`\bigl(`|
|\Bigl|$\Bigl($|`\Bigl(`|
|\bigm|$\bigm\vert$|`\bigm\vert`|
|\Bigm|$\Bigm\vert$|`\Bigm\vert`|
|\bigodot|$\bigodot$||
|\bigominus|<span style="color:firebrick;">Not supported</span>|[Issue #1222](https://github.com/KaTeX/KaTeX/issues/1222)|
|\bigoplus|$\bigoplus$||
|\bigoslash|<span style="color:firebrick;">Not supported</span>|[Issue #1222](https://github.com/KaTeX/KaTeX/issues/1222)|
|\bigotimes|$\bigotimes$||
|\bigr|$\bigr)$|`\bigr)`|
|\Bigr|$\Bigr)$|`\Bigr)`|
|\bigsqcap|<span style="color:firebrick;">Not supported</span>|[Issue #1222](https://github.com/KaTeX/KaTeX/issues/1222)|
|\bigsqcup|$\bigsqcup$||
|\bigstar|$\bigstar$||
|\bigtriangledown|$\bigtriangledown$||
|\bigtriangleup|$\bigtriangleup$||
|\biguplus|$\biguplus$||
|\bigvee|$\bigvee$||
|\bigwedge|$\bigwedge$||
|\binom|$\binom n k$|`\binom n k`|
|\blacklozenge|$\blacklozenge$||
|\blacksquare|$\blacksquare$||
|\blacktriangle|$\blacktriangle$||
|\blacktriangledown|$\blacktriangledown$||
|\blacktriangleleft|$\blacktriangleleft$||
|\blacktriangleright|$\blacktriangleright$||
|\bm|$\bm{AaBb}$|`\bm{AaBb}`|
|{Bmatrix}|$\begin{Bmatrix}a&b\\c&d\end{Bmatrix}$|`\begin{Bmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{Bmatrix}`|
|{Bmatrix*}|$\begin{Bmatrix*}[r]0&-1\\-1&0\end{Bmatrix*}$|`\begin{Bmatrix*}[r]`<br>&nbsp;&nbsp;&nbsp;`0 & -1 \\`<br>&nbsp;&nbsp;&nbsp;`-1 & 0`<br>`\end{Bmatrix*}`|
|{bmatrix}|$\begin{bmatrix}a&b\\c&d\end{bmatrix}$|`\begin{bmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{bmatrix}`|
|{bmatrix*}|$\begin{bmatrix*}[r]0&-1\\-1&0\end{bmatrix*}$|`\begin{bmatrix*}[r]`<br>&nbsp;&nbsp;&nbsp;`0 & -1 \\`<br>&nbsp;&nbsp;&nbsp;`-1 & 0`<br>`\end{bmatrix*}`|
|\bmod|$a \bmod b$|`a \bmod b`|
|\bold|$\bold{AaBb123}$|`\bold{AaBb123}`|
|\boldsymbol|$\boldsymbol{AaBb}$|`\boldsymbol{AaBb}`|
|\bot|$\bot$||
|\bowtie|$\bowtie$||
|\Box|$\Box$||
|\boxdot|$\boxdot$||
|\boxed|$\boxed{ab}$|`\boxed{ab}`|
|\boxminus|$\boxminus$||
|\boxplus|$\boxplus$||
|\boxtimes|$\boxtimes$||
|\Bra|$\Bra{\psi}$|`\Bra{\psi}`|
|\bra|$\bra{\psi}$|`\bra{\psi}`|
|\braket|$\braket{\phi\VERT\psi}$|<code>\braket{\phi&#124;\psi}</code>|
|\Braket|$\Braket{ ϕ \VERT \frac{∂^2}{∂ t^2} \VERT ψ }$| <code>\Braket{ ϕ &#124; \frac{∂^2}{∂ t^2} &#124; ψ }</code>|
|\brace|${n\brace k}$|`{n\brace k}`|
|\bracevert|<span style="color:firebrick;">Not supported</span>||
|\brack|${n\brack k}$|`{n\brack k}`|
|\breve|$\breve{eu}$|`\breve{eu}`|
|\buildrel|<span style="color:firebrick;">Not supported</span>||
|\bull|$\bull$||
|\bullet|$\bullet$||
|\Bumpeq|$\Bumpeq$||
|\bumpeq|$\bumpeq$||

## C

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\C|<span style="color:firebrick;">Not supported</span>|[Deprecated](https://en.wikipedia.org/wiki/Help:Displaying_a_formula#Deprecated_syntax)|
|\cal|$\cal AaBb123$|`\cal AaBb123`|
|\cancel|$\cancel{5}$|`\cancel{5}`|
|\cancelto|<span style="color:firebrick;">Not supported</span>||
|\Cap|$\Cap$||
|\cap|$\cap$||
|{cases}|$\begin{cases}a&\text{if }b\\c&\text{if }d\end{cases}$|`\begin{cases}`<br>&nbsp;&nbsp;&nbsp;`a &\text{if } b  \\`<br>&nbsp;&nbsp;&nbsp;`c &\text{if } d`<br>`\end{cases}`|
|\cases|<span style="color:firebrick;">Not supported</span>|see `{cases}`|
|{CD}|$$\begin{CD}A @>a>> B \\@VbVV @AAcA\\C @= D\end{CD}$$|`\begin{CD}`<br>&nbsp;&nbsp;&nbsp;`A  @>a>>  B  \\`<br>`@VbVV    @AAcA \\`<br>&nbsp;&nbsp;&nbsp;`C  @=     D`<br>`\end{CD}`|
|\cdot|$\cdot$||
|\cdotp|$\cdotp$||
|\cdots|$\cdots$||
|\ce |${\mathrm{C}{\vphantom{X}}_{\smash[t]{6}}\mathrm{H}{\vphantom{X}}_{\smash[t]{5}}{-}\mathrm{CHO}}$|`\ce{C6H5-CHO}` Requires an [extension](https://github.com/KaTeX/KaTeX/tree/main/contrib/mhchem/)|
|\cee|<span style="color:firebrick;">Not supported</span>|Deprecated by mhchem
|\centerdot|$a\centerdot b$|`a\centerdot b`|
|\cf|<span style="color:firebrick;">Not supported</span>|Deprecated by mhchem;
use `\ce` instead|
|\cfrac|$\cfrac{2}{1+\cfrac{2}{1+\cfrac{2}{1}}}$|`\cfrac{2}{1+\cfrac{2}{1+\cfrac{2}{1}}}`|
|\char|$\char"263a$|`\char"263a`|
|\check|$\check{oe}$|`\check{oe}`|
|\ch|$\ch$||
|\checkmark|$\checkmark$||
|\Chi|$\Chi$||
|\chi|$\chi$||
|\choose|${n+1 \choose k+2}$|`{n+1 \choose k+2}`|
|\circ|$\circ$||
|\circeq|$\circeq$||
|\circlearrowleft|$\circlearrowleft$||
|\circlearrowright|$\circlearrowright$||
|\circledast|$\circledast$||
|\circledcirc|$\circledcirc$||
|\circleddash|$\circleddash$||
|\circledR|$\circledR$||
|\circledS|$\circledS$||
|\class|<span style="color:firebrick;">Not supported</span>|A PR is pending.
|\cline|<span style="color:firebrick;">Not supported</span>|[Issue #269](https://github.com/KaTeX/KaTeX/issues/269)|
|\clubs|$\clubs$||
|\clubsuit|$\clubsuit$||
|\cnums|$\cnums$||
|\colon|$\colon$||
|\Colonapprox|$\Colonapprox$||
|\colonapprox|$\colonapprox$||
|\coloncolon|$\coloncolon$||
|\coloncolonapprox|$\coloncolonapprox$||
|\coloncolonequals|$\coloncolonequals$||
|\coloncolonminus|$\coloncolonminus$||
|\coloncolonsim|$\coloncolonsim$||
|\Coloneq|$\Coloneq$||
|\coloneq|$\coloneq$||
|\colonequals|$\colonequals$||
|\Coloneqq|$\Coloneqq$||
|\coloneqq|$\coloneqq$||
|\colonminus|$\colonminus$||
|\Colonsim|$\Colonsim$||
|\colonsim|$\colonsim$||
|\color|$\color{#0000FF} AaBb123$|`\color{#0000FF} AaBb123`|
|\colorbox|$\colorbox{red}{Black on red}$|`\colorbox{red}{Black on red}`|
|\complement|$\complement$||
|\Complex|$\Complex$||
|\cong|$\cong$||
|\Coppa|<span style="color:firebrick;">Not supported</span>||
|\coppa|<span style="color:firebrick;">Not supported</span>||
|\coprod|$\coprod$||
|\copyright|$\copyright$||
|\cos|$\cos$||
|\cosec|$\cosec$||
|\cosh|$\cosh$||
|\cot|$\cot$||
|\cotg|$\cotg$||
|\coth|$\coth$||
|\cr|$\begin{matrix} a & b\cr c & d \end{matrix}$|`\begin{matrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \cr`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{matrix}`|
|\csc|$\csc$||
|\cssId|<span style="color:firebrick;">Not supported</span>|A PR is pending.
|\ctg|$\ctg$||
|\cth|$\cth$||
|\Cup|$\Cup$||
|\cup|$\cup$||
|\curlyeqprec|$\curlyeqprec$||
|\curlyeqsucc|$\curlyeqsucc$||
|\curlyvee|$\curlyvee$||
|\curlywedge|$\curlywedge$||
|\curvearrowleft|$\curvearrowleft$||
|\curvearrowright|$\curvearrowright$||

## D

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\dag|$\dag$||
|\Dagger|$\Dagger$||
|\dagger|$\dagger$||
|\daleth|$\daleth$||
|\Darr|$\Darr$||
|\dArr|$\dArr$||
|\darr|$\darr$||
{darray}|$\begin{darray}{cc}a&b\\c&d\end{darray}$ | `\begin{darray}{cc}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{darray}`|
|\dashleftarrow|$\dashleftarrow$||
|\dashrightarrow|$\dashrightarrow$||
|\dashv|$\dashv$||
|\dbinom|$\dbinom n k$|`\dbinom n k`|
|\dblcolon|$\dblcolon$||
|{dcases}|$\begin{dcases}a&\text{if }b\\c&\text{if }d\end{dcases}$|`\begin{dcases}`<br>&nbsp;&nbsp;&nbsp;`a &\text{if } b  \\`<br>&nbsp;&nbsp;&nbsp;`c &\text{if } d`<br>`\end{dcases}`|
|\ddag|$\ddag$||
|\ddagger|$\ddagger$||
|\ddddot|$\ddddot x$|`\ddddot x`|
|\dddot|$\dddot x$|`\dddot x`|
|\ddot|$\ddot x$|`\ddot x`|
|\ddots|$\ddots$||
|\DeclareMathOperator|<span style="color:firebrick;">Not supported</span>||
|\def|$\def\foo{x^2} \foo + \foo$|`\def\foo{x^2} \foo + \foo`|
|\definecolor|<span style="color:firebrick;">Not supported</span>|[Issue #750](https://github.com/KaTeX/KaTeX/issues/750)|
|\deg|$\deg$||
|\degree|$\degree$||
|\delta|$\delta$||
|\Delta|$\Delta$||
|\det|$\det$||
|\Digamma|<span style="color:firebrick;">Not supported</span>||
|\digamma|$\digamma$||
|\dfrac|$\dfrac{a-1}{b-1}$|`\dfrac{a-1}{b-1}`|
|\diagdown|$\diagdown$||
|\diagup|$\diagup$||
|\Diamond|$\Diamond$||
|\diamond|$\diamond$||
|\diamonds|$\diamonds$||
|\diamondsuit|$\diamondsuit$||
|\dim|$\dim$||
|\displaylines|<span style="color:firebrick;">Not supported</span>||
|\displaystyle|$\displaystyle\sum_0^n$|`\displaystyle\sum_0^n`|
|\div|$\div$||
|\divideontimes|$\divideontimes$||
|\dot|$\dot x$|`\dot x`|
|\Doteq|$\Doteq$||
|\doteq|$\doteq$||
|\doteqdot|$\doteqdot$||
|\dotplus|$\dotplus$||
|\dots|$x_1 + \dots + x_n$|`x_1 + \dots + x_n`|
|\dotsb|$x_1 +\dotsb + x_n$|`x_1 +\dotsb + x_n`|
|\dotsc|$x,\dotsc,y$|`x,\dotsc,y`|
|\dotsi|$$\int_{A_1}\int_{A_2}\dotsi$$|`\int_{A_1}\int_{A_2}\dotsi`|
|\dotsm|$x_1 x_2 \dotsm x_n$|`$x_1 x_2 \dotsm x_n`|
|\dotso|$\dotso$||
|\doublebarwedge|$\doublebarwedge$||
|\doublecap|$\doublecap$||
|\doublecup|$\doublecup$||
|\Downarrow|$\Downarrow$||
|\downarrow|$\downarrow$||
|\downdownarrows|$\downdownarrows$||
|\downharpoonleft|$\downharpoonleft$||
|\downharpoonright|$\downharpoonright$||
|{drcases}|$\begin{drcases}a&\text{if }b\\c&\text{if }d\end{drcases}$|`\begin{drcases}`<br>&nbsp;&nbsp;&nbsp;`a &\text{if } b  \\`<br>&nbsp;&nbsp;&nbsp;`c &\text{if } d`<br>`\end{drcases}`|

## E

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\edef|$\def\foo{a}\edef\fcopy{\foo}\def\foo{}\fcopy$|`\def\foo{a}\edef\fcopy{\foo}\def\foo{}\fcopy`|
|\ell|$\ell$||
|\else|<span style="color:firebrick;">Not supported</span>|[Issue #1003](https://github.com/KaTeX/KaTeX/issues/1003)|
|\em|<span style="color:firebrick;">Not supported</span>||
|\emph|$\emph{nested \emph{emphasis}}$|`\emph{nested \emph{emphasis}}`|
|\empty|$\empty$||
|\emptyset|$\emptyset$||
|\enclose|<span style="color:firebrick;">Not supported</span>|Non standard
|\end|$\begin{matrix} a & b\\ c & d\end{matrix}$|`\begin{matrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{matrix}`|
|\endgroup|${a\endgroup$|`{a\endgroup`|
|\enspace|$a\enspace b$|`a\enspace b`|
|\Epsilon|$\Epsilon$||
|\epsilon|$\epsilon$||
|\eqalign|<span style="color:firebrick;">Not supported</span>||
|\eqalignno|<span style="color:firebrick;">Not supported</span>||
|\eqcirc|$\eqcirc$||
|\Eqcolon|$\Eqcolon$||
|\eqcolon|$\eqcolon$||
|{equation}|$$\begin{equation}a = b + c\end{equation}$$|`\begin{equation}`<br>&nbsp;&nbsp;&nbsp;`a = b + c`<br>`\end{equation}`|
|{equation*}|$$\begin{equation*}a = b + c\end{equation*}$$|`\begin{equation*}`<br>&nbsp;&nbsp;&nbsp;`a = b + c`<br>`\end{equation*}`|
|{eqnarray}|<span style="color:firebrick;">Not supported</span>||
|\Eqqcolon|$\Eqqcolon$||
|\eqqcolon|$\eqqcolon$||
|\eqref|<span style="color:firebrick;">Not supported</span>|[Issue #350](https://github.com/KaTeX/KaTeX/issues/350)|
|\eqsim|$\eqsim$||
|\eqslantgtr|$\eqslantgtr$||
|\eqslantless|$\eqslantless$||
|\equalscolon|$\equalscolon$||
|\equalscoloncolon|$\equalscoloncolon$||
|\equiv|$\equiv$||
|\Eta|$\Eta$||
|\eta|$\eta$||
|\eth|$\eth$||
|\euro|<span style="color:firebrick;">Not supported</span>||
|\exist|$\exist$||
|\exists|$\exists$||
|\exp|$\exp$||
|\expandafter|||

## F

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\fallingdotseq|$\fallingdotseq$||
|\fbox|$\fbox{Hi there!}$|`\fbox{Hi there!}`|
|\fcolorbox|$\fcolorbox{red}{aqua}{A}$|`\fcolorbox{red}{aqua}{A}`|
|\fi|<span style="color:firebrick;">Not supported</span>|[Issue #1003](https://github.com/KaTeX/KaTeX/issues/1003)|
|\Finv|$\Finv$||
|\flat|$\flat$||
|\footnotesize|$\footnotesize footnotesize$|`\footnotesize footnotesize`|
|\forall|$\forall$||
|\frac|$\frac a b$|`\frac a b`|
|\frak|$\frak{AaBb}$|`\frak{AaBb}`|
|\frown|$\frown$||
|\futurelet|||

## G

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\Game|$\Game$||
|\Gamma|$\Gamma$||
|\gamma|$\gamma$||
|{gather}|$$\begin{gather}a=b\\e=b+c\end{gather}$$|`\begin{gather}`<br>&nbsp;&nbsp;&nbsp;`a=b \\ `<br>&nbsp;&nbsp;&nbsp;`e=b+c`<br>`\end{gather}`|
|{gathered}|$\begin{gathered}a=b\\e=b+c\end{gathered}$|`\begin{gathered}`<br>&nbsp;&nbsp;&nbsp;`a=b \\ `<br>&nbsp;&nbsp;&nbsp;`e=b+c`<br>`\end{gathered}`|
|\gcd|$\gcd$||
|\gdef|$\gdef\sqr#1{#1^2} \sqr{y} + \sqr{y}$|`\gdef\sqr#1{#1^2} \sqr{y} + \sqr{y}`|
|\ge|$\ge$||
|\geneuro|<span style="color:firebrick;">Not supported</span>||
|\geneuronarrow|<span style="color:firebrick;">Not supported</span>||
|\geneurowide|<span style="color:firebrick;">Not supported</span>||
|\genfrac|$\genfrac ( ] {2pt}{0}a{a+1}$|`\genfrac ( ] {2pt}{0}a{a+1}`|
|\geq|$\geq$||
|\geqq|$\geqq$||
|\geqslant|$\geqslant$||
|\gets|$\gets$||
|\gg|$\gg$||
|\ggg|$\ggg$||
|\gggtr|$\gggtr$||
|\gimel|$\gimel$||
|\global|$\global\def\add#1#2{#1+#2} \add 2 3$|`\global\def\add#1#2{#1+#2} \add 2 3`|
|\gnapprox|$\gnapprox$||
|\gneq|$\gneq$||
|\gneqq|$\gneqq$||
|\gnsim|$\gnsim$||
|\grave|$\grave{eu}$|`\grave{eu}`|
|\gt|$a \gt b$|`a \gt b`|
|\gtrdot|$\gtrdot$||
|\gtrapprox|$\gtrapprox$||
|\gtreqless|$\gtreqless$||
|\gtreqqless|$\gtreqqless$||
|\gtrless|$\gtrless$||
|\gtrsim|$\gtrsim$||
|\gvertneqq|$\gvertneqq$||

## H

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\H|$\text{\H{a}}$|`\text{\H{a}}`|
|\Harr|$\Harr$||
|\hArr|$\hArr$||
|\harr|$\harr$||
|\hat|$\hat{\theta}$|`\hat{\theta}`|
|\hbar|$\hbar$||
|\hbox|$\hbox{$x^2$}$|`\hbox{$x^2$}`|
|\hbox to <dimen>| <span style="color:firebrick;">Not supported</span> ||
|\hdashline|$\begin{matrix}a&b\\ \hdashline c &d\end{matrix}$|`\begin{matrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`\hdashline`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{matrix}`|
|\hearts|$\hearts$||
|\heartsuit|$\heartsuit$||
|\hfil|<span style="color:firebrick;">Not supported</span>||
|\hfill|<span style="color:firebrick;">Not supported</span>|Issues [#164](https://github.com/KaTeX/KaTeX/issues/164) & [#269](https://github.com/KaTeX/KaTeX/issues/269)|
|\hline|$\begin{matrix}a&b\\ \hline c &d\end{matrix}$|`\begin{matrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\ \hline`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{matrix}`|
|\hom|$\hom$||
|\hookleftarrow|$\hookleftarrow$||
|\hookrightarrow|$\hookrightarrow$||
|\hphantom|$a\hphantom{bc}d$|`a\hphantom{bc}d`|
|\href|$\href{https://katex.org/}{\KaTeX}$|`\href{https://katex.org/}{\KaTeX}` Requires `trust` [option](options.md)|
|\hskip|$w\hskip1em i\hskip2em d$|`w\hskip1em i\hskip2em d`|
|\hslash|$\hslash$||
|\hspace|$s\hspace7ex k$|`s\hspace7ex k`|
|\htmlClass|$\htmlClass{foo}{x}$|`\htmlClass{foo}{x}` Must enable `trust` and disable `strict` [option](options.md)|
|\htmlData|$\htmlData{foo=a, bar=b}{x}$|`\htmlData{foo=a, bar=b}{x}` Must enable `trust` and disable `strict` [option](options.md)|
|\htmlId|$\htmlId{bar}{x}$|`\htmlId{bar}{x}` Must enable `trust` and disable `strict` [option](options.md)|
|\htmlStyle|$\htmlStyle{color: red;}{x}$|`\htmlStyle{color: red;}{x}` Must enable `trust` and disable `strict` [option](options.md)|
|\huge|$\huge huge$|`\huge huge`|
|\Huge|$\Huge Huge$|`\Huge Huge`|

## I

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\i|$\text{\i}$|`\text{\i}`|
|\idotsint|<span style="color:firebrick;">Not supported</span>||
|\iddots|<span style="color:firebrick;">Not supported</span>|[Issue #1223](https://github.com/KaTeX/KaTeX/issues/1223)|
|\if|<span style="color:firebrick;">Not supported</span>|[Issue #1003](https://github.com/KaTeX/KaTeX/issues/1003)|
|\iff|$A\iff B$|`A\iff B`|
|\ifmode|<span style="color:firebrick;">Not supported</span>|[Issue #1003](https://github.com/KaTeX/KaTeX/issues/1003)|
|\ifx|<span style="color:firebrick;">Not supported</span>|[Issue #1003](https://github.com/KaTeX/KaTeX/issues/1003)|
|\iiiint|<span style="color:firebrick;">Not supported</span>||
|\iiint|$\iiint$||
|\iint|$\iint$||
|\Im|$\Im$||
|\image|$\image$||
|\imageof|$\imageof$||
|\imath|$\imath$||
|\impliedby|$P\impliedby Q$|`P\impliedby Q`|
|\implies|$P\implies Q$|`P\implies Q`|
|\in|$\in$||
|\includegraphics|$\includegraphics[height=0.8em, totalheight=0.9em, width=0.9em, alt=KA logo]{https://cdn.kastatic.org/images/apple-touch-icon-57x57-precomposed.new.png}$|`\includegraphics[height=0.8em, totalheight=0.9em, width=0.9em, alt=KA logo]{https://cdn.kastatic.org/images/apple-touch-icon-57x57-precomposed.new.png}` Requires `trust` [option](options.md)
|\inf|$\inf$||
|\infin|$\infin$||
|\infty|$\infty$||
|\injlim|$\injlim$| `\injlim` |
|\int|$\int$||
|\intercal|$\intercal$||
|\intop|$\intop$||
|\Iota|$\Iota$||
|\iota|$\iota$||
|\isin|$\isin$||
|\it|${\it AaBb}$|`{\it AaBb}`|
|\itshape|<span style="color:firebrick;">Not supported</span>||

## JK

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\j|$\text{\j}$|`\text{\j}`|
|\jmath|$\jmath$||
|\Join|$\Join$||
|\Kappa|$\Kappa$||
|\kappa|$\kappa$||
|\KaTeX|$\KaTeX$||
|\ker|$\ker$||
|\kern|$I\kern-2.5pt R$|`I\kern-2.5pt R`|
|\Ket|$\Ket{\psi}$|`\Ket{\psi}`|
|\ket|$\ket{\psi}$|`\ket{\psi}`|
|\Koppa|<span style="color:firebrick;">Not supported</span>||
|\koppa|<span style="color:firebrick;">Not supported</span>||

## L

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\L|<span style="color:firebrick;">Not supported</span>||
|\l|<span style="color:firebrick;">Not supported</span>||
|\Lambda|$\Lambda$||
|\lambda|$\lambda$||
|\label|<span style="color:firebrick;">Not supported</span>||
|\land|$\land$||
|\lang|$\lang A\rangle$|`\lang A\rangle`|
|\langle|$\langle A\rangle$|`\langle A\rangle`|
|\Larr|$\Larr$||
|\lArr|$\lArr$||
|\larr|$\larr$||
|\large|$\large large$|`\large large`|
|\Large|$\Large Large$|`\Large Large`|
|\LARGE|$\LARGE LARGE$|`\LARGE LARGE`|
|\LaTeX|$\LaTeX$||
|\lBrace|$\lBrace$||
|\lbrace|$\lbrace$||
|\lbrack|$\lbrack$||
|\lceil|$\lceil$||
|\ldotp|$\ldotp$||
|\ldots|$\ldots$||
|\le|$\le$||
|\leadsto|$\leadsto$||
|\left|$\left\lbrace \dfrac ab \right.$|`\left\lbrace \dfrac ab \right.`|
|\leftarrow|$\leftarrow$||
|\Leftarrow|$\Leftarrow$||
|\LeftArrow|<span style="color:firebrick;">Not supported</span>|Non standard
|\leftarrowtail|$\leftarrowtail$||
|\leftharpoondown|$\leftharpoondown$||
|\leftharpoonup|$\leftharpoonup$||
|\leftleftarrows|$\leftleftarrows$||
|\Leftrightarrow|$\Leftrightarrow$||
|\leftrightarrow|$\leftrightarrow$||
|\leftrightarrows|$\leftrightarrows$||
|\leftrightharpoons|$\leftrightharpoons$||
|\leftrightsquigarrow|$\leftrightsquigarrow$||
|\leftroot|<span style="color:firebrick;">Not supported</span>||
|\leftthreetimes|$\leftthreetimes$||
|\leq|$\leq$||
|\leqalignno|<span style="color:firebrick;">Not supported</span>||
|\leqq|$\leqq$||
|\leqslant|$\leqslant$||
|\lessapprox|$\lessapprox$||
|\lessdot|$\lessdot$||
|\lesseqgtr|$\lesseqgtr$||
|\lesseqqgtr|$\lesseqqgtr$||
|\lessgtr|$\lessgtr$||
|\lesssim|$\lesssim$||
|\let|||
|\lfloor|$\lfloor$||
|\lg|$\lg$||
|\lgroup|$\lgroup$||
|\lhd|$\lhd$||
|\lim|$\lim$||
|\liminf|$\liminf$||
|\limits|$\lim\limits_x$|`\lim\limits_x`|
|\limsup|$\limsup$||
|\ll|$\ll$||
|\llap|${=}\llap{/\,}$|`{=}\llap{/\,}`|
|\llbracket|$\llbracket$||
|\llcorner|$\llcorner$||
|\Lleftarrow|$\Lleftarrow$||
|\lll|$\lll$||
|\llless|$\llless$||
|\lmoustache|$\lmoustache$||
|\ln|$\ln$||
|\lnapprox|$\lnapprox$||
|\lneq|$\lneq$||
|\lneqq|$\lneqq$||
|\lnot|$\lnot$||
|\lnsim|$\lnsim$||
|\log|$\log$||
|\long|||
|\Longleftarrow|$\Longleftarrow$||
|\longleftarrow|$\longleftarrow$||
|\Longleftrightarrow|$\Longleftrightarrow$||
|\longleftrightarrow|$\longleftrightarrow$||
|\longmapsto|$\longmapsto$||
|\Longrightarrow|$\Longrightarrow$||
|\longrightarrow|$\longrightarrow$||
|\looparrowleft|$\looparrowleft$||
|\looparrowright|$\looparrowright$||
|\lor|$\lor$||
|\lower|<span style="color:firebrick;">Not supported</span>||
|\lozenge|$\lozenge$||
|\lparen|$\lparen$||
|\Lrarr|$\Lrarr$||
|\lrArr|$\lrArr$||
|\lrarr|$\lrarr$||
|\lrcorner|$\lrcorner$||
|\lq|$\lq$||
|\Lsh|$\Lsh$||
|\lt|$\lt$||
|\ltimes|$\ltimes$||
|\lVert|$\lVert$||
|\lvert|$\lvert$||
|\lvertneqq|$\lvertneqq$||

## M

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\maltese|$\maltese$||
|\mapsto|$\mapsto$||
|\mathbb|$\mathbb{AB}$|`\mathbb{AB}`<br>KaTeX supports A-Z k|
|\mathbf|$\mathbf{AaBb123}$|`\mathbf{AaBb123}`|
|\mathbin|$a\mathbin{!}b$|`a\mathbin{!}b`|
|\mathcal|$\mathcal{AaBb123}$|`\mathcal{AaBb123}`|
|\mathchoice|$a\mathchoice{\,}{\,\,}{\,\,\,}{\,\,\,\,}b$|`a\mathchoice{\,}{\,\,}{\,\,\,}{\,\,\,\,}b`|
|\mathclap|$\displaystyle\sum_{\mathclap{1\le i\le n}} x_{i}$|`\sum_{\mathclap{1\le i\le n}} x_{i}`|
|\mathclose|$a + (b\mathclose\gt + c$|`a + (b\mathclose\gt + c`|
|\mathellipsis|$\mathellipsis$||
|\mathfrak|$\mathfrak{AaBb}$|`\mathfrak{AaBb}`<br>KaTeX supports A-Za-z|
|\mathinner|$ab\mathinner{\text{inside}}cd$|`ab\mathinner{\text{inside}}cd`|
|\mathit|$\mathit{AaBb}$|`\mathit{AaBb}`<br>KaTeX supports A-Za-z|
|\mathllap|${=}\mathllap{/\,}$|`{=}\mathllap{/\,}`|
|\mathnormal|$\mathnormal{AaBb}$|`\mathnormal{AaBb}`<br>KaTeX supports A-Za-z|
|\mathop|$\mathop{\star}_a^b$|`\mathop{\star}_a^b`|
|\mathopen|$a + \mathopen\lt b) + c$|`a + \mathopen\lt b) + c`|
|\mathord|$1\mathord{,}234{,}567$|`1\mathord{,}234{,}567`|
|\mathpunct|$A\mathpunct{-}B$|`A\mathpunct{-}B`|
|\mathrel|$a \mathrel{\#} b$|`a \mathrel{\#} b`|
|\mathrlap|$\mathrlap{\,/}{=}$|`\mathrlap{\,/}{=}`|
|\mathring|$\mathring{a}$|`\mathring{a}`|
|\mathrm|$\mathrm{AaBb123}$|`\mathrm{AaBb123}`|
|\mathscr|$\mathscr{AB}$|`\mathscr{AaBb123}`<br>KaTeX supports A-Z|
|\mathsf|$\mathsf{AaBb123}$|`\mathsf{AaBb123}`|
|\mathsterling|$\mathsterling$||
|\mathstrut|$\sqrt{\mathstrut a}$|`\sqrt{\mathstrut a}`|
|\mathtip|<span style="color:firebrick;">Not supported</span>||
|\mathtt|$\mathtt{AaBb123}$|`\mathtt{AaBb123}`|
|\matrix|<span style="color:firebrick;">Not supported</span>|See `{matrix}`|
|{matrix}|$\begin{matrix}a&b\\c&d\end{matrix}$|`\begin{matrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{matrix}`|
|{matrix*}|$\begin{matrix*}[r]0&-1\\-1&0\end{matrix*}$|`\begin{matrix*}[r]`<br>&nbsp;&nbsp;&nbsp;`0 & -1 \\`<br>&nbsp;&nbsp;&nbsp;`-1 & 0`<br>`\end{matrix*}`|
|\max|$\max$||
|\mbox|<span style="color:firebrick;">Not supported</span>||
|\md|<span style="color:firebrick;">Not supported</span>||
|\mdseries|<span style="color:firebrick;">Not supported</span>||
|\measuredangle|$\measuredangle$||
|\medspace|$a\medspace b$|`a\medspace b`|
|\mho|$\mho$||
|\mid|$\{x∈ℝ\mid x>0\}$|`\{x∈ℝ\mid x>0\}`|
|\middle|$P\left(A\middle\vert B\right)$|`P\left(A\middle\vert B\right)`|
|\min|$\min$||
|\minuscolon|$\minuscolon$||
|\minuscoloncolon|$\minuscoloncolon$||
|\minuso|$\minuso$||
|\mit|<span style="color:firebrick;">Not supported</span>|See `\mathit`|
|\mkern|$a\mkern18mu b$|`a\mkern18mu b`|
|\mmlToken|<span style="color:firebrick;">Not supported</span>||
|\mod|$3\equiv 5 \mod 2$|`3\equiv 5 \mod 2`|
|\models|$\models$||
|\moveleft|<span style="color:firebrick;">Not supported</span>||
|\moveright|<span style="color:firebrick;">Not supported</span>||
|\mp|$\mp$||
|\mskip|$a\mskip{10mu}b$|`a\mskip{10mu}b`|
|\mspace|<span style="color:firebrick;">Not supported</span>||
|\Mu|$\Mu$||
|\mu|$\mu$||
|\multicolumn|<span style="color:firebrick;">Not supported</span>|[Issue #269](https://github.com/KaTeX/KaTeX/issues/269)|
|{multiline}|<span style="color:firebrick;">Not supported</span>||
|\multimap|$\multimap$||

## N

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\N|$\N$||
|\nabla|$\nabla$||
|\natnums|$\natnums$||
|\natural|$\natural$||
|\negmedspace|$a\negmedspace b$|`a\negmedspace b`|
|\ncong|$\ncong$||
|\ne|$\ne$||
|\nearrow|$\nearrow$||
|\neg|$\neg$||
|\negthickspace|$a\negthickspace b$|`a\negthickspace b`|
|\negthinspace|$a\negthinspace b$|`a\negthinspace b`|
|\neq|$\neq$||
|\newcommand|$\newcommand\chk{\checkmark} \chk$|`\newcommand\chk{\checkmark} \chk`|
|\newenvironment|<span style="color:firebrick;">Not supported</span>|[Issue #37](https://github.com/KaTeX/KaTeX/issues/37)|
|\Newextarrow|<span style="color:firebrick;">Not supported</span>||
|\newline|$a\newline b$|`a\newline b`|
|\nexists|$\nexists$||
|\ngeq|$\ngeq$||
|\ngeqq|$\ngeqq$||
|\ngeqslant|$\ngeqslant$||
|\ngtr|$\ngtr$||
|\ni|$\ni$||
|\nleftarrow|$\nleftarrow$||
|\nLeftarrow|$\nLeftarrow$||
|\nLeftrightarrow|$\nLeftrightarrow$||
|\nleftrightarrow|$\nleftrightarrow$||
|\nleq|$\nleq$||
|\nleqq|$\nleqq$||
|\nleqslant|$\nleqslant$||
|\nless|$\nless$||
|\nmid|$\nmid$||
|\nobreak|||
|\nobreakspace|$a\nobreakspace b$|`a\nobreakspace b`|
|\noexpand|||
|\nolimits|$\lim\nolimits_x$|`\lim\nolimits_x`|
|\nonumber|$$\begin{align}a&=b+c\nonumber\\d+e&=f\end{align}$$|`\begin{align}`<br>&nbsp;&nbsp;&nbsp;`a&=b+c \nonumber\\`<br>&nbsp;&nbsp;&nbsp;`d+e&=f`<br>`\end{align}`|
|\normalfont|<span style="color:firebrick;">Not supported</span>||
|\normalsize|$\normalsize normalsize$|`\normalsize normalsize`|
|\not|$\not =$|`\not =`|
|\notag|$$\begin{align}a&=b+c\notag\\d+e&=f\end{align}$$|`\begin{align}`<br>&nbsp;&nbsp;&nbsp;`a&=b+c \notag\\`<br>&nbsp;&nbsp;&nbsp;`d+e&=f`<br>`\end{align}`|
|\notin|$\notin$||
|\notni|$\notni$||
|\nparallel|$\nparallel$||
|\nprec|$\nprec$||
|\npreceq|$\npreceq$||
|\nRightarrow|$\nRightarrow$||
|\nrightarrow|$\nrightarrow$||
|\nshortmid|$\nshortmid$||
|\nshortparallel|$\nshortparallel$||
|\nsim|$\nsim$||
|\nsubseteq|$\nsubseteq$||
|\nsubseteqq|$\nsubseteqq$||
|\nsucc|$\nsucc$||
|\nsucceq|$\nsucceq$||
|\nsupseteq|$\nsupseteq$||
|\nsupseteqq|$\nsupseteqq$||
|\ntriangleleft|$\ntriangleleft$||
|\ntrianglelefteq|$\ntrianglelefteq$||
|\ntriangleright|$\ntriangleright$||
|\ntrianglerighteq|$\ntrianglerighteq$||
|\Nu|$\Nu$||
|\nu|$\nu$||
|\nVDash|$\nVDash$||
|\nVdash|$\nVdash$||
|\nvDash|$\nvDash$||
|\nvdash|$\nvdash$||
|\nwarrow|$\nwarrow$||

## O

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\O|$\text{\O}$|`\text{\O}`|
|\o|$\text{\o}$|`\text{\o}`|
|\odot|$\odot$||
|\OE|$\text{\OE}$|`\text{\OE}`|
|\oe|$\text{\oe}$|`\text{\oe}`|
|\officialeuro|<span style="color:firebrick;">Not supported</span>||
|\oiiint|$\oiiint$||
|\oiint|$\oiint$||
|\oint|$\oint$||
|\oldstyle|<span style="color:firebrick;">Not supported</span>||
|\omega|$\omega$||
|\Omega|$\Omega$||
|\Omicron|$\Omicron$||
|\omicron|$\omicron$||
|\ominus|$\ominus$||
|\operatorname|$\operatorname{asin} x$|`\operatorname{asin} x`|
|\operatorname\*|$\operatorname*{asin}\limits_y x$|`\operatorname*{asin}\limits_y x`|
|\operatornamewithlimits|$\operatornamewithlimits{asin}\limits_y x$|`\operatornamewithlimits{asin}\limits_y x`|
|\oplus|$\oplus$||
|\or|<span style="color:firebrick;">Not supported</span>||
|\origof|$\origof$||
|\oslash|$\oslash$||
|\otimes|$\otimes$||
|\over|${a+1 \over b+2}+c$|`{a+1 \over b+2}+c`|
|\overbrace|$\overbrace{x+⋯+x}^{n\text{ times}}$|`\overbrace{x+⋯+x}^{n\text{ times}}`|
|\overbracket|<span style="color:firebrick;">Not supported</span>||
|\overgroup|$\overgroup{AB}$|`\overgroup{AB}`|
|\overleftarrow|$\overleftarrow{AB}$|`\overleftarrow{AB}`|
|\overleftharpoon|$\overleftharpoon{AB}$|`\overleftharpoon{AB}`|
|\overleftrightarrow|$\overleftrightarrow{AB}$|`\overleftrightarrow{AB}`|
|\overline|$\overline{\text{a long argument}}$|`\overline{\text{a long argument}}`|
|\overlinesegment|$\overlinesegment{AB}$|`\overlinesegment{AB}`|
|\overparen|<span style="color:firebrick;">Not supported</span>|See `\overgroup`|
|\Overrightarrow|$\Overrightarrow{AB}$|`\Overrightarrow{AB}`|
|\overrightarrow|$\overrightarrow{AB}$|`\overrightarrow{AB}`|
|\overrightharpoon|$\overrightharpoon{ac}$|`\overrightharpoon{ac}`|
|\overset|$\overset{!}{=}$|`\overset{!}{=}`|
|\overwithdelims|<span style="color:firebrick;">Not supported</span>||
|\owns|$\owns$||

## P

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\P|$\text{\P}$|`\text{\P}`|
|\pagecolor|<span style="color:firebrick;">Not supported</span>|[Deprecated](https://en.wikipedia.org/wiki/Help:Displaying_a_formula#Deprecated_syntax)|
|\parallel|$\parallel$||
|\part|<span style="color:firebrick;">Not supported</span>|[Deprecated](https://en.wikipedia.org/wiki/Help:Displaying_a_formula#Deprecated_syntax)|
|\partial|$\partial$||
|\perp|$\perp$||
|\phantom|$\Gamma^{\phantom{i}j}_{i\phantom{j}k}$|`\Gamma^{\phantom{i}j}_{i\phantom{j}k}`|
|\phase|$\phase{-78^\circ}$|`\phase{-78^\circ}`|
|\Phi|$\Phi$||
|\phi|$\phi$||
|\Pi|$\Pi$||
|\pi|$\pi$||
|{picture}|<span style="color:firebrick;">Not supported</span>||
|\pitchfork|$\pitchfork$||
|\plim|$\plim$||
|\plusmn|$\plusmn$||
|\pm|$\pm$||
|\pmatrix|<span style="color:firebrick;">Not supported</span>|See `{pmatrix}`|
|{pmatrix}|$\begin{pmatrix}a&b\\c&d\end{pmatrix}$|`\begin{pmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{pmatrix}`
|{pmatrix*}|$\begin{pmatrix*}[r]0&-1\\-1&0\end{pmatrix*}$|`\begin{pmatrix*}[r]`<br>&nbsp;&nbsp;&nbsp;`0 & -1 \\`<br>&nbsp;&nbsp;&nbsp;`-1 & 0`<br>`\end{pmatrix*}`|
|\pmb|$\pmb{\mu}$|`\pmb{\mu}`|
|\pmod|$x\pmod a$|`x\pmod a`|
|\pod|$x \pod a$|`x \pod a`|
|\pounds|$\pounds$||
|\Pr|$\Pr$||
|\prec|$\prec$||
|\precapprox|$\precapprox$||
|\preccurlyeq|$\preccurlyeq$||
|\preceq|$\preceq$||
|\precnapprox|$\precnapprox$||
|\precneqq|$\precneqq$||
|\precnsim|$\precnsim$||
|\precsim|$\precsim$||
|\prime|$\prime$||
|\prod|$\prod$||
|\projlim|$\projlim$|`\projlim`|
|\propto|$\propto$||
|\providecommand|$\providecommand\greet{\text{Hello}} \greet$|`\providecommand\greet{\text{Hello}} \greet`|
|\psi|$\psi$||
|\Psi|$\Psi$||
|\pu |${123~\mathchoice{\textstyle\frac{\mathrm{kJ}}{\mathrm{mol}}}{\frac{\mathrm{kJ}}{\mathrm{mol}}}{\frac{\mathrm{kJ}}{\mathrm{mol}}}{\frac{\mathrm{kJ}}{\mathrm{mol}}}}$|`\pu{123 kJ//mol}` Requires an [extension](https://github.com/KaTeX/KaTeX/tree/main/contrib/mhchem/)|

## QR

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\Q|<span style="color:firebrick;">Not supported</span>|See `\Bbb{Q}`|
|\qquad|$a\qquad\qquad{b}$|`a\qquad\qquad{b}`|
|\quad|$a\quad\quad{b}$|`a\quad\quad{b}`|
|\R|$\R$||
|\r|$\text{\r{a}}$|`\text{\r{a}}`|
|\raise|<span style="color:firebrick;">Not supported</span>|see `\raisebox`|
|\raisebox|$h\raisebox{2pt}{ighe}r$|`h\raisebox{2pt}{$ighe$}r`|
|\rang|$\langle A\rang$|`\langle A\rang`|
|\rangle|$\langle A\rangle$|`\langle A\rangle`|
|\Rarr|$\Rarr$||
|\rArr|$\rArr$||
|\rarr|$\rarr$||
|\ratio|$\ratio$||
|\rBrace|$\rBrace$||
|\rbrace|$\rbrace$||
|\rbrack|$\rbrack$||
|{rcases}|$\begin{rcases}a&\text{if }b\\c&\text{if }d\end{rcases}$|`\begin{rcases}`<br>&nbsp;&nbsp;&nbsp;`a &\text{if } b  \\`<br>&nbsp;&nbsp;&nbsp;`c &\text{if } d`<br>`\end{rcases}`|
|\rceil|$\rceil$||
|\Re|$\Re$||
|\real|$\real$||
|\Reals|$\Reals$||
|\reals|$\reals$||
|\ref|<span style="color:firebrick;">Not supported</span>|[Issue #350](https://github.com/KaTeX/KaTeX/issues/350)|
|\relax|||
|\renewcommand|$\def\hail{Hi!}\renewcommand\hail{\text{Ahoy!}} \hail$|`\def\hail{Hi!}`<br>`\renewcommand\hail{\text{Ahoy!}}`<br>`\hail`|
|\renewenvironment|<span style="color:firebrick;">Not supported</span>||
|\require|<span style="color:firebrick;">Not supported</span>||
|\restriction|$\restriction$||
|\rfloor|$\rfloor$||
|\rgroup|$\rgroup$||
|\rhd|$\rhd$||
|\Rho|$\Rho$||
|\rho|$\rho$||
|\right|$\left.\dfrac a b\right)$|`\left.\dfrac a b\right)`|
|\Rightarrow|$\Rightarrow$||
|\rightarrow|$\rightarrow$||
|\rightarrowtail|$\rightarrowtail$||
|\rightharpoondown|$\rightharpoondown$||
|\rightharpoonup|$\rightharpoonup$||
|\rightleftarrows|$\rightleftarrows$||
|\rightleftharpoons|$\rightleftharpoons$||
|\rightrightarrows|$\rightrightarrows$||
|\rightsquigarrow|$\rightsquigarrow$||
|\rightthreetimes|$\rightthreetimes$||
|\risingdotseq|$\risingdotseq$||
|\rlap|$\rlap{\,/}{=}$|`\rlap{\,/}{=}`|
|\rm|$\rm AaBb12$|`\rm AaBb12`|
|\rmoustache|$\rmoustache$||
|\root|<span style="color:firebrick;">Not supported</span>||
|\rotatebox|<span style="color:firebrick;">Not supported</span>|[Issue #681](https://github.com/KaTeX/KaTeX/issues/681)|
|\rparen|$\rparen$||
|\rq|$\rq$||
|\rrbracket|$\rrbracket$||
|\Rrightarrow|$\Rrightarrow$||
|\Rsh|$\Rsh$||
|\rtimes|$\rtimes$||
|\Rule|<span style="color:firebrick;">Not supported</span>|see `\rule`
|\rule|$x\rule[6pt]{2ex}{1ex}x$|`x\rule[6pt]{2ex}{1ex}x`|
|\rVert|$\rVert$||
|\rvert|$\rvert$||

## S

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\S|$\text{\S}$|`\text{\S}`|
|\Sampi|<span style="color:firebrick;">Not supported</span>||
|\sampi|<span style="color:firebrick;">Not supported</span>||
|\sc|<span style="color:firebrick;">Not supported</span>|[Issue #471](https://github.com/KaTeX/KaTeX/issues/471)|
|\scalebox|<span style="color:firebrick;">Not supported</span>||
|\scr|<span style="color:firebrick;">Not supported</span>|See `\mathscr`|
|\scriptscriptstyle|$\scriptscriptstyle \frac cd$|`\scriptscriptstyle \frac cd`|
|\scriptsize|$\scriptsize scriptsize$|`\scriptsize scriptsize`|
|\scriptstyle|$\frac ab + {\scriptstyle \frac cd}$|`\frac ab + {\scriptstyle \frac cd}`|
|\sdot|$\sdot$||
|\searrow|$\searrow$||
|\sec|$\sec$||
|\sect|$\text{\sect}$|`\text{\sect}`|
|\set|$\set{x\VERT x<5}$|<code>\set{x&#124;x<5}</code> |
|\Set|$\Set{ x \VERT x<\frac 1 2 }$ | <code>\Set{ x &#124; x<\frac 1 2}</code> |
|\setlength|<span style="color:firebrick;">Not supported</span>|[Issue #687](https://github.com/KaTeX/KaTeX/issues/687)|
|\setminus|$\setminus$||
|\sf|$\sf AaBb123$|`\sf AaBb123`|
|\sharp|$\sharp$||
|\shortmid|$\shortmid$||
|\shortparallel|$\shortparallel$||
|\shoveleft|<span style="color:firebrick;">Not supported</span>||
|\shoveright|<span style="color:firebrick;">Not supported</span>||
|\sideset|<span style="color:firebrick;">Not supported</span>||
|\Sigma|$\Sigma$||
|\sigma|$\sigma$||
|\sim|$\sim$||
|\simcolon|$\simcolon$||
|\simcoloncolon|$\simcoloncolon$||
|\simeq|$\simeq$||
|\sin|$\sin$||
|\sinh|$\sinh$||
|\sixptsize|$\sixptsize sixptsize$|`\sixptsize sixptsize`|
|\sh|$\sh$||
|\skew|<span style="color:firebrick;">Not supported</span>||
|\skip|<span style="color:firebrick;">Not supported</span>||
|\sl|<span style="color:firebrick;">Not supported</span>||
|\small|$\small small$|`\small small`|
|\smallfrown|$\smallfrown$||
|\smallint|$\smallint$||
|{smallmatrix}|$\begin{smallmatrix} a & b \\ c & d \end{smallmatrix}$|`\begin{smallmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{smallmatrix}`|
|\smallsetminus|$\smallsetminus$||
|\smallsmile|$\smallsmile$||
|\smash|$\left(x^{\smash{2}}\right)$|`\left(x^{\smash{2}}\right)`|
|\smile|$\smile$||
|\smiley|<span style="color:firebrick;">Not supported</span>||
|\sout|$\sout{abc}$|`\sout{abc}`|
|\Space|<span style="color:firebrick;">Not supported</span>|see `\space`
|\space|$a\space b$|`a\space b`|
|\spades|$\spades$||
|\spadesuit|$\spadesuit$||
|\sphericalangle|$\sphericalangle$||
|{split}|$$\begin{equation}\begin{split}a &=b+c\\&=e+f\end{split}\end{equation}$$|`\begin{equation}`<br>`\begin{split}`<br>&nbsp;&nbsp;&nbsp;`a &=b+c\\`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`&=e+f`<br>`\end{split}`<br>`\end{equation}`|
|\sqcap|$\sqcap$||
|\sqcup|$\sqcup$||
|\square|$\square$||
|\sqrt|$\sqrt[3]{x}$|`\sqrt[3]{x}`|
|\sqsubset|$\sqsubset$||
|\sqsubseteq|$\sqsubseteq$||
|\sqsupset|$\sqsupset$||
|\sqsupseteq|$\sqsupseteq$||
|\ss|$\text{\ss}$|`\text{\ss}`|
|\stackrel|$\stackrel{!}{=}$|`\stackrel{!}{=}`|
|\star|$\star$||
|\Stigma|<span style="color:firebrick;">Not supported</span>||
|\stigma|<span style="color:firebrick;">Not supported</span>||
|\strut|<span style="color:firebrick;">Not supported</span>||
|\style|<span style="color:firebrick;">Not supported</span>|Non standard|
|\sub|$\sub$||
|{subarray}|<span style="color:firebrick;">Not supported</span>||
|\sube|$\sube$||
|\Subset|$\Subset$||
|\subset|$\subset$||
|\subseteq|$\subseteq$||
|\subseteqq|$\subseteqq$||
|\subsetneq|$\subsetneq$||
|\subsetneqq|$\subsetneqq$||
|\substack|$$\sum_{\substack{0<i<m\\0<j<n}}$$|`\sum_{\substack{0<i<m\\0<j<n}}`|
|\succ|$\succ$||
|\succapprox|$\succapprox$||
|\succcurlyeq|$\succcurlyeq$||
|\succeq|$\succeq$||
|\succnapprox|$\succnapprox$||
|\succneqq|$\succneqq$||
|\succnsim|$\succnsim$||
|\succsim|$\succsim$||
|\sum|$\sum$||
|\sup|$\sup$||
|\supe|$\supe$||
|\Supset|$\Supset$||
|\supset|$\supset$||
|\supseteq|$\supseteq$||
|\supseteqq|$\supseteqq$||
|\supsetneq|$\supsetneq$||
|\supsetneqq|$\supsetneqq$||
|\surd|$\surd$||
|\swarrow|$\swarrow$||

## T

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\tag|$$\tag{3.1c} a^2+b^2=c^2$$|`\tag{3.1c} a^2+b^2=c^2`|
|\tag*|$$\tag*{3.1c} a^2+b^2=c^2$$|`\tag*{3.1c} a^2+b^2=c^2`|
|\tan|$\tan$||
|\tanh|$\tanh$||
|\Tau|$\Tau$||
|\tau|$\tau$||
|\tbinom|$\tbinom n k$|`\tbinom n k`|
|\TeX|$\TeX$||
|\text|$\text{ yes }\&\text{ no }$|`\text{ yes }\&\text{ no }`|
|\textasciitilde|$\text{\textasciitilde}$|`\text{\textasciitilde}`|
|\textasciicircum|$\text{\textasciicircum}$|`\text{\textasciicircum}`|
|\textbackslash|$\text{\textbackslash}$|`\text{\textbackslash}`|
|\textbar|$\text{\textbar}$|`\text{\textbar}`|
|\textbardbl|$\text{\textbardbl}$|`\text{\textbardbl}`|
|\textbf|$\textbf{AaBb123}$|`\textbf{AaBb123}`|
|\textbraceleft|$\text{\textbraceleft}$|`\text{\textbraceleft}`|
|\textbraceright|$\text{\textbraceright}$|`\text{\textbraceright}`|
|\textcircled|$\text{\textcircled a}$|`\text{\textcircled a}`|
|\textcolor|$\textcolor{blue}{F=ma}$|`\textcolor{blue}{F=ma}`|
|\textdagger|$\text{\textdagger}$|`\text{\textdagger}`|
|\textdaggerdbl|$\text{\textdaggerdbl}$|`\text{\textdaggerdbl}`|
|\textdegree|$\text{\textdegree}$|`\text{\textdegree}`|
|\textdollar|$\text{\textdollar}$|`\text{\textdollar}`|
|\textellipsis|$\text{\textellipsis}$|`\text{\textellipsis}`|
|\textemdash|$\text{\textemdash}$|`\text{\textemdash}`|
|\textendash|$\text{\textendash}$|`\text{\textendash}`|
|\textgreater|$\text{\textgreater}$|`\text{\textgreater}`|
|\textit|$\textit{AaBb}$|`\textit{AaBb}`|
|\textless|$\text{\textless}$|`\text{\textless}`|
|\textmd|$\textmd{AaBb123}$|`\textmd{AaBb123}`|
|\textnormal|$\textnormal{AB}$|`\textnormal{AB}`|
|\textquotedblleft|$\text{\textquotedblleft}$|`\text{\textquotedblleft}`|
|\textquotedblright|$\text{\textquotedblright}$|`\text{\textquotedblright}`|
|\textquoteleft|$\text{\textquoteleft}$|`\text{\textquoteleft}`|
|\textquoteright|$\text{\textquoteright}$|`\text{\textquoteright}`|
|\textregistered|$\text{\textregistered}$|`\text{\textregistered}`|
|\textrm|$\textrm{AaBb123}$|`\textrm{AaBb123}`|
|\textsc|<span style="color:firebrick;">Not supported</span>|[Issue #471](https://github.com/KaTeX/KaTeX/issues/471)|
|\textsf|$\textsf{AaBb123}$|`\textsf{AaBb123}`|
|\textsl|<span style="color:firebrick;">Not supported</span>||
|\textsterling|$\text{\textsterling}$|`\text{\textsterling}`|
|\textstyle|$\textstyle\sum_0^n$|`\textstyle\sum_0^n`|
|\texttip|<span style="color:firebrick;">Not supported</span>||
|\texttt|$\texttt{AaBb123}$|`\texttt{AaBb123}`|
|\textunderscore|$\text{\textunderscore}$|`\text{\textunderscore}`|
|\textup|$\textup{AaBb123}$|`\textup{AaBb123}`|
|\textvisiblespace|<span style="color:firebrick;">Not supported</span>||
|\tfrac|$\tfrac ab$|`\tfrac ab`|
|\tg|$\tg$||
|\th|$\th$||
|\therefore|$\therefore$||
|\Theta|$\Theta$||
|\theta|$\theta$||
|\thetasym|$\thetasym$||
|\thickapprox|$\thickapprox$||
|\thicksim|$\thicksim$||
|\thickspace|$a\thickspace b$|`a\thickspace b`|
|\thinspace|$a\thinspace b$|`a\thinspace b`|
|\tilde|$\tilde M$|`\tilde M`|
|\times|$\times$||
|\Tiny|<span style="color:firebrick;">Not supported</span>|see `\tiny`|
|\tiny|$\tiny tiny$|`\tiny tiny`|
|\to|$\to$||
|\toggle|<span style="color:firebrick;">Not supported</span>||
|\top|$\top$||
|\triangle|$\triangle$||
|\triangledown|$\triangledown$||
|\triangleleft|$\triangleleft$||
|\trianglelefteq|$\trianglelefteq$||
|\triangleq|$\triangleq$||
|\triangleright|$\triangleright$||
|\trianglerighteq|$\trianglerighteq$||
|\tt|${\tt AaBb123}$|`{\tt AaBb123}`|
|\twoheadleftarrow|$\twoheadleftarrow$||
|\twoheadrightarrow|$\twoheadrightarrow$||

## U

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\u|$\text{\u{a}}$|`\text{\u{a}}`|
|\Uarr|$\Uarr$||
|\uArr|$\uArr$||
|\uarr|$\uarr$||
|\ulcorner|$\ulcorner$||
|\underbar|$\underbar{X}$|`\underbar{X}`|
|\underbrace|$\underbrace{x+⋯+x}_{n\text{ times}}$|`\underbrace{x+⋯+x}_{n\text{ times}}`|
|\underbracket|<span style="color:firebrick;">Not supported</span>||
|\undergroup|$\undergroup{AB}$|`\undergroup{AB}`|
|\underleftarrow|$\underleftarrow{AB}$|`\underleftarrow{AB}`|
|\underleftrightarrow|$\underleftrightarrow{AB}$|`\underleftrightarrow{AB}`|
|\underrightarrow|$\underrightarrow{AB}$|`\underrightarrow{AB}`|
|\underline|$\underline{\text{a long argument}}$|`\underline{\text{a long argument}}`|
|\underlinesegment|$\underlinesegment{AB}$|`\underlinesegment{AB}`|
|\underparen|<span style="color:firebrick;">Not supported</span>|See `\undergroup`|
|\underrightarrow|$\underrightarrow{AB}$|`\underrightarrow{AB}`|
|\underset|$\underset{!}{=}$|`\underset{!}{=}`|
|\unicode|<span style="color:firebrick;">Not supported</span>||
|\unlhd|$\unlhd$||
|\unrhd|$\unrhd$||
|\up|<span style="color:firebrick;">Not supported</span>||
|\Uparrow|$\Uparrow$||
|\uparrow|$\uparrow$||
|\Updownarrow|$\Updownarrow$||
|\updownarrow|$\updownarrow$||
|\upharpoonleft|$\upharpoonleft$||
|\upharpoonright|$\upharpoonright$||
|\uplus|$\uplus$||
|\uproot|<span style="color:firebrick;">Not supported</span>||
|\upshape|<span style="color:firebrick;">Not supported</span>||
|\Upsilon|$\Upsilon$||
|\upsilon|$\upsilon$||
|\upuparrows|$\upuparrows$||
|\urcorner|$\urcorner$||
|\url|$\footnotesize\url{https://katex.org/}$|`\url{https://katex.org/}` Requires `trust` [option](options.md)|
|\utilde|$\utilde{AB}$|`\utilde{AB}`|

## V

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\v|$\text{\v{a}}$|`\text{\v{a}}`|
|\varcoppa|<span style="color:firebrick;">Not supported</span>||
|\varDelta|$\varDelta$||
|\varepsilon|$\varepsilon$||
|\varGamma|$\varGamma$||
|\varinjlim|$\varinjlim$|`\varinjlim`|
|\varkappa|$\varkappa$||
|\varLambda|$\varLambda$||
|\varliminf|$\varliminf$|`\varliminf`|
|\varlimsup|$\varlimsup$|`\varlimsup`|
|\varnothing|$\varnothing$||
|\varOmega|$\varOmega$||
|\varPhi|$\varPhi$||
|\varphi|$\varphi$||
|\varPi|$\varPi$||
|\varpi|$\varpi$||
|\varprojlim|$\varprojlim$|`\varprojlim`|
|\varpropto|$\varpropto$||
|\varPsi|$\varPsi$||
|\varrho|$\varrho$||
|\varSigma|$\varSigma$||
|\varsigma|$\varsigma$||
|\varstigma|<span style="color:firebrick;">Not supported</span>||
|\varsubsetneq|$\varsubsetneq$||
|\varsubsetneqq|$\varsubsetneqq$||
|\varsupsetneq|$\varsupsetneq$||
|\varsupsetneqq|$\varsupsetneqq$||
|\varTheta|$\varTheta$||
|\vartheta|$\vartheta$||
|\vartriangle|$\vartriangle$||
|\vartriangleleft|$\vartriangleleft$||
|\vartriangleright|$\vartriangleright$||
|\varUpsilon|$\varUpsilon$||
|\varXi|$\varXi$||
|\vcentcolon|$\mathrel{\vcentcolon =}$|`\mathrel{\vcentcolon =}`|
|\vcenter|$a+\left(\vcenter{\frac{\frac a b}c}\right)$|`a+\left(\vcenter{\hbox{$\frac{\frac a b}c$}}\right)`<br>TeX (strict) syntax|
|\vcenter|$a+\left(\vcenter{\frac{\frac a b}c}\right)$|`a+\left(\vcenter{\frac{\frac a b}c}\right)`<br>non-strict syntax|
|\Vdash|$\Vdash$||
|\vDash|$\vDash$||
|\vdash|$\vdash$||
|\vdots|$\vdots$||
|\vec|$\vec{F}$|`\vec{F}`|
|\vee|$\vee$||
|\veebar|$\veebar$||
|\verb|$\verb!\frac a b!$|`\verb!\frac a b!`|
|\Vert|$\Vert$||
|\vert|$\vert$||
|\vfil|<span style="color:firebrick;">Not supported</span>||
|\vfill|<span style="color:firebrick;">Not supported</span>||
|\vline|<span style="color:firebrick;">Not supported</span>|[Issue #269](https://github.com/KaTeX/KaTeX/issues/269)|
|{Vmatrix}|$\begin{Vmatrix}a&b\\c&d\end{Vmatrix}$|`\begin{Vmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{Vmatrix}`|
|{Vmatrix*}|$\begin{Vmatrix*}[r]0&-1\\-1&0\end{Vmatrix*}$|`\begin{Vmatrix*}[r]`<br>&nbsp;&nbsp;&nbsp;`0 & -1 \\`<br>&nbsp;&nbsp;&nbsp;`-1 & 0`<br>`\end{Vmatrix*}`|
|{vmatrix}|$\begin{vmatrix}a&b\\c&d\end{vmatrix}$|`\begin{vmatrix}`<br>&nbsp;&nbsp;&nbsp;`a & b \\`<br>&nbsp;&nbsp;&nbsp;`c & d`<br>`\end{vmatrix}`|
|{vmatrix*}|$\begin{vmatrix*}[r]0&-1\\-1&0\end{vmatrix*}$|`\begin{vmatrix*}[r]`<br>&nbsp;&nbsp;&nbsp;`0 & -1 \\`<br>&nbsp;&nbsp;&nbsp;`-1 & 0`<br>`\end{vmatrix*}`|
|\vphantom|$\overline{\vphantom{M}a}$|`\overline{\vphantom{M}a}`|
|\Vvdash|$\Vvdash$||

## W

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\wedge|$\wedge$||
|\weierp|$\weierp$||
|\widecheck|$\widecheck{AB}$|`\widecheck{AB}`|
|\widehat|$\widehat{AB}$|`\widehat{AB}`|
|\wideparen|<span style="color:firebrick;">Not supported</span>|[Issue #560](https://github.com/KaTeX/KaTeX/issues/560)|
|\widetilde|$\widetilde{AB}$|`\widetilde{AB}`|
|\wp|$\wp$||
|\wr|$\wr$||

## X

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\xcancel|$\xcancel{ABC}$|`\xcancel{ABC}`|
|\xdef|$\def\foo{a}\xdef\fcopy{\foo}\def\foo{}\fcopy$|`\def\foo{a}\xdef\fcopy{\foo}\def\foo{}\fcopy`|
|\Xi|$\Xi$||
|\xi|$\xi$||
|\xhookleftarrow|$\xhookleftarrow{abc}$|`\xhookleftarrow{abc}`|
|\xhookrightarrow|$\xhookrightarrow{abc}$|`\xhookrightarrow{abc}`|
|\xLeftarrow|$\xLeftarrow{abc}$|`\xLeftarrow{abc}`|
|\xleftarrow|$\xleftarrow{abc}$|`\xleftarrow{abc}`|
|\xleftharpoondown|$\xleftharpoondown{abc}$|`\xleftharpoondown{abc}`|
|\xleftharpoonup|$\xleftharpoonup{abc}$|`\xleftharpoonup{abc}`|
|\xLeftrightarrow|$\xLeftrightarrow{abc}$|`\xLeftrightarrow{abc}`|
|\xleftrightarrow|$\xleftrightarrow{abc}$|`\xleftrightarrow{abc}`|
|\xleftrightharpoons|$\xleftrightharpoons{abc}$|`\xleftrightharpoons{abc}`|
|\xlongequal|$\xlongequal{abc}$|`\xlongequal{abc}`|
|\xmapsto|$\xmapsto{abc}$|`\xmapsto{abc}`|
|\xRightarrow|$\xRightarrow{abc}$|`\xRightarrow{abc}`|
|\xrightarrow|$\xrightarrow{abc}$|`\xrightarrow{abc}`|
|\xrightharpoondown|$\xrightharpoondown{abc}$|`\xrightharpoondown{abc}`|
|\xrightharpoonup|$\xrightharpoonup{abc}$|`\xrightharpoonup{abc}`|
|\xrightleftharpoons|$\xrightleftharpoons{abc}$|`\xrightleftharpoons{abc}`|
|\xtofrom|$\xtofrom{abc}$|`\xtofrom{abc}`|
|\xtwoheadleftarrow|$\xtwoheadleftarrow{abc}$|`\xtwoheadleftarrow{abc}`|
|\xtwoheadrightarrow|$\xtwoheadrightarrow{abc}$|`\xtwoheadrightarrow{abc}`|

## YZ

|Symbol/Function |  Rendered   | Source or Comment|
|:---------------|:------------|:-----------------|
|\yen|$\yen$||
|\Z|$\Z$||
|\Zeta|$\Zeta$||
|\zeta|$\zeta$||
