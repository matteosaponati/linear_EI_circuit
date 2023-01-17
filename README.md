# spontaneous gamma dynamics implemented in a noisy damped harmonic oscillator

this is a repository for the paper:
<br/> "*Spontaneous variability in gamma dynamics described by a damped harmonic oscillator driven by noise*"<br/>
G Spyropoulos, **M Saponati**, JR Dowdall, ML Schölvinck, CA Bosman, B Lima, A Peter, I Onorato, J Klon-Lipok, R Roese, S Neuenschwander, W Singer, P Fries, M Vinck <br/>
(2022, Nature Communications)
https://www.nature.com/articles/s41467-022-29674-x

## dependencies
all the simulations use [Python 3.8]. The scripts require [numpy] and [matplotlib].

## usage
the project has a pip-installable package. How to set it up:

- `git clone` the repository 
- `pip install -e . `

## structure  

the modules of the package are in `utils/`.

* `main` <br/>
(default args as in the paper, optional args: beta1, beta2, total number of timesteps `time`, the four elements of the affine transformation matrix A listed as `[[a1,a2],[a3,a4]]`)<br/>
`python main {} {} {} {} {} {} {}` <br/>
outputs: <br/>
`results/num_solution_ar.npy`: numerical solution of AR(2) model <br/>
`results/num_solution_ei.npy`: numerical solution of (E,I) system obtained with the affine transformation

* scripts to replicate the results shown in the related figure<br/>
`python suppfig_1` (optional arg: affine matrix `A`) <br/>
`python suppfig_2` (optional args: `beta1`, `beta2``, number of timesteps `time`, affine matrix `A) <br/>
`python suppfig_3` (optional args: (optional args: `beta1`, `beta2`, number of timesteps `time`, affine matrix `A`) <br/><br/>
The plots are located in `/plots`


 ## citation and credits
Spyropoulos, G., Saponati, M., Dowdall, J. R., Schölvinck, M. L., Bosman, C. A., Lima, B., ... & Vinck, M. (2022). 
**Spontaneous variability in gamma dynamics described by a damped harmonic oscillator driven by noise**. Nature communications, 13(1), 1-18.<br/>
```
@article{spyropoulos2022spontaneous,
  title={Spontaneous variability in gamma dynamics described by a damped harmonic oscillator driven by noise},
  author={Spyropoulos, Georgios and Saponati, Matteo and Dowdall, Jarrod Robert and Sch{\"o}lvinck, Marieke Louise and Bosman, Conrado Arturo and Lima, Bruss and Peter, Alina and Onorato, Irene and Klon-Lipok, Johanna and Roese, Rasmus and others},
  journal={Nature communications},
  volume={13},
  number={1},
  pages={1--18},
  year={2022},
  publisher={Nature Publishing Group}
}
```


