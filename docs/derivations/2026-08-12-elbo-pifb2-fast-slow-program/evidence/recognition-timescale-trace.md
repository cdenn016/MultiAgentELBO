# Recognition-density and timescale trace

PIFB2 explicitly treats ((q_i,p_i)) as the fast subsystem and ((s_i,r_i)) as slow. Its stated
hierarchy puts (q_i) on the perceptual-inference timescale, (p_i) on a learning/M-step scale,
(s_i) on a slower model-learning scale, frames slower still, and (r_i) as fixed hyperpriors.

Older Friston terminology calls the variational density over hidden causes or states the
**recognition density**. Modern equivalent terms are variational density and approximate posterior.
Friston's D/E/M separation supports the qualitative inference-versus-learning hierarchy, but it
does not by itself prove a singular-perturbation reduction for this model.

Typing rule: if (s_i) is a law over model parameter (m_i), it is a slow parameter-recognition or
model-belief section. The generative model is the normalized kernel (p_i(o_i,k_i\mid m_i)).
Observation expectations use a joint (zeta_i(dk_i,dm_i)), with (q_i\otimes s_i) only under an
explicit mean-field restriction.

Primary sources:

- Friston, *Hierarchical Models in the Brain* (2008), PMC2570625.
- Friston et al., *Reinforcement Learning or Active Inference?* (2009), PMC2713351.
- Friston et al., *Free Energy, Precision and Learning* (2014), PMC4235126.

Live source trace: `PIFB2.tex:929-952`; exact typing repair:
`Research/manuscripts/magent_elbo_whitepaper/09_pifb2_crosswalk.tex:8-77`.
