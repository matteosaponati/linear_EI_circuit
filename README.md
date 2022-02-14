# spontaneous gamma dynamics implemented in a noisy damped harmonic oscillator

this is a repository for the paper:
<br/> "*Spontaneous variability in gamma dynamics described by a linear harmonic oscillator driven by noise*"<br/>
G Spyropoulos, M Saponati, JR Dowdall, ML Schölvinck, CA Bosman, B Lima, A Peter, I Onorato, J Klon-Lipok, R Roese, S Neuenschwander, W Singer, P Fries, M Vinck <br/>
(2022, Nature Communications)
[[BiorXiv]](https://www.biorxiv.org/content/10.1101/793729v2.abstract)

## dependencies
the code is written in [Python 3.x], requires [numpy] and [matplotlib]

## usage
just `git clone` the repository to your computer.

## structure  

* `main` <br/>
(default args as in the paper)<br/>
run with 4 optional args: beta1, beta2, the affine transformation matrix A (list of 4 elements `[a1,a2,a3,a4]`), total number of timesteps T
`python main {} {} {} {}` <br/>
outputs: <br/>
`num_solution_ar.npy`: numerical solution of AR(2) model <br/>
`num_solution_ei.npy`: numerical solution of (E,I) system obtained with the affine transformation

* scripts to replicate the results shown in the related figure<br/>
`python supp1` (optional args: beta1, beta2, affine matrix A, number of timesteps T) <br/>
`python supp2` (optional arg: affine matrix A) <br/>
`python supp3` (optional args: (optional args: beta1, beta2, affine matrix A) 

 <!--- ## citation and credits
Spyropoulos, G., Saponati, M., Dowdall, J. R., Schölvinck, M. L., Bosman, C. A., Lima, B., ... & Fries, P. (2020). **Spontaneous variability in gamma dynamics described by a damped harmonic oscillator driven by noise**. bioRxiv, 793729. <br/>

```
@article{spyropoulos2020spontaneous,
  title={Spontaneous variability in gamma dynamics described by a linear harmonic oscillator driven by noise},
  author={Spyropoulos, Georgios and Dowdall, Jarrod Robert and Sch{\"o}lvinck, Marieke Louise and Bosman, Conrado Arturo and Lima, Bruss and Peter, Alina and Onorato, Irene and Klon-Lipok, Johanna and Roese, Rasmus and Neuenschwander, Sergio and others},
  journal={bioRxiv},
  pages={793729},
  year={2020},
  publisher={Cold Spring Harbor Laboratory}
} -->
```


