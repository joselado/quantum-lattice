#!/usr/bin/env python3
"""ql-extras.py - plots for the "Hopf insulator and tilings" mode (interface-pyqt/hopftilings); run as python3, no chmod needed.

Computes with the standalone scripts in extras/ (ql_hopf_insulator, ql_tilings, ql_tiling_spectra, ql_chair44_chains) and plots the
result.  Unlike most ql-* scripts it computes its own data instead of reading .OUT files, because the quantities are cheap, have no
pyqula Hamiltonian to hand over, and are specific to this mode.  --png PATH saves the figure instead of opening a window.

    python3 ql-extras.py hopf-invariant --h 2.0
    python3 ql-extras.py hopf-gap --hmax 4.5
    python3 ql-extras.py hopf-slab --h 2.0 --layers 12
    python3 ql-extras.py tiling --kind spectre --level 2
    python3 ql-extras.py tiling-spectrum --kind spectre --level 2 --hopping unit
    python3 ql-extras.py chair44-chain --line axis --depth 12 --lam 1.0 --nlines 6
"""
import argparse
import os
import sys

import numpy as np

here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, here)
sys.path.insert(0, os.path.join(here, "..", "extras"))

import matplotlib
if "--png" in sys.argv: matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotstyle
plotstyle.apply()
plt.rcParams.update({"font.size":10,"axes.labelsize":10,"xtick.labelsize":9,"ytick.labelsize":9}) # plotstyle's sizes are for single-panel plots

p = argparse.ArgumentParser()
p.add_argument("task")
p.add_argument("--png", default="")
p.add_argument("--h", type=float, default=2.0)
p.add_argument("--hmax", type=float, default=4.5)
p.add_argument("--layers", type=int, default=12)
p.add_argument("--kind", default="spectre")
p.add_argument("--level", type=int, default=2)
p.add_argument("--hopping", default="unit")
p.add_argument("--line", default="axis")
p.add_argument("--depth", type=int, default=12)
p.add_argument("--lam", type=float, default=1.0)
p.add_argument("--nlines", type=int, default=6)
a = p.parse_args()


def finish(fig):
  fig.set_facecolor(plotstyle.BACKGROUND)
  fig.tight_layout()
  if a.png: fig.savefig(a.png,dpi=110)
  else: plt.show()


if a.task == "hopf-invariant":
  import ql_hopf_insulator as HI
  hs = np.linspace(-a.hmax,a.hmax,37)
  hs = np.unique(np.r_[hs,a.h])
  hs = hs[np.min(np.abs(hs[:,None]-np.array([-3,-1,1,3.])[None,:]),axis=1)>0.03] # skip the gap closings
  inv = np.array([HI.hopf_invariant_degree(h,32) for h in hs])
  fig,ax = plt.subplots(figsize=(7,4))
  ax.plot(hs,inv,"o",ms=3)
  ax.axvline(a.h,color="tab:red",lw=0.8)
  ax.set_xlabel("h"); ax.set_ylabel("Hopf invariant (degree of z/|z|)")
  ax.set_title("h = %.2f: invariant %+.3f" % (a.h,HI.hopf_invariant_degree(a.h,48)),fontsize=9)
  finish(fig)
elif a.task == "hopf-gap":
  import ql_hopf_insulator as HI
  hs = np.linspace(-a.hmax,a.hmax,61)
  gap = np.array([HI.bulk_gap(h,12) for h in hs])
  fig,ax = plt.subplots(figsize=(7,4))
  ax.plot(hs,gap)
  ax.set_xlabel("h"); ax.set_ylabel("bulk gap (coarse k grid)")
  ax.set_title("the gap closes at h = -3, -1, 1, 3",fontsize=9)
  finish(fig)
elif a.task == "hopf-slab":
  import ql_hopf_insulator as HI
  x,E,Wt = HI.slab_spectrum(a.h,a.layers)
  fig,ax = plt.subplots(figsize=(7,4.5))
  sc = None
  for j in range(E.shape[1]): sc = ax.scatter(x,E[:,j],c=Wt[:,j],cmap="viridis",vmin=0,vmax=1,s=4)
  ax.set_xlabel("Gamma - X - M - Gamma"); ax.set_ylabel("energy")
  ax.set_title("slab, %d layers, h=%.2f; colour = weight on the outer 2 layers per side" % (a.layers,a.h),fontsize=8)
  fig.colorbar(sc,ax=ax)
  finish(fig)
elif a.task in ("tiling","tiling-spectrum"):
  import ql_tilings as T
  import ql_tiling_spectra as S
  patch = T.planar_patch(a.kind,a.level)
  if a.task == "tiling":
    fig,ax = plt.subplots(figsize=(6,6))
    for u,v in patch.edges: ax.plot(*patch.vert[[u,v]].T,color="0.6",lw=0.6)
    ax.plot(*patch.vert.T,"o",ms=1.5)
    ax.set_aspect("equal"); ax.set_title("%s, level %d: %d sites, %d bonds" % (a.kind,a.level,len(patch.vert),len(patch.edges)),fontsize=9)
    finish(fig)
  else:
    w,ipr = S.eig(T.tight_binding(patch,a.hopping))
    n = len(w)
    fig,ax = plt.subplots(1,2,figsize=(10,4))
    h,e = np.histogram(w,bins=100,density=True)
    ax[0].step(0.5*(e[1:]+e[:-1]),h); ax[0].set_xlabel("E"); ax[0].set_ylabel("DOS")
    ax[1].scatter(w,ipr*n,s=3); ax[1].set_xlabel("E"); ax[1].set_ylabel("N * IPR")
    ax[0].set_title("%s, level %d, %s hopping, %d sites" % (a.kind,a.level,a.hopping,n),fontsize=9)
    finish(fig)
elif a.task == "chair44-chain":
  import ql_chair44_chains as Ch
  res = {}
  for sh in (False,True): res[sh] = Ch.stats(a.line,sh,nlines=a.nlines,n=a.depth,lam=a.lam)
  fig,ax = plt.subplots(1,3,figsize=(11,3.8))
  for j,key,lab in ((0,"nipr","N * IPR (4096 sites)"),(1,"ly","Lyapunov exponent (E = 0.3, 1.0)"),(2,"maxsum","max |partial sum| of the onsite energies")):
    for k,sh in enumerate((False,True)):
      ax[j].plot(np.full(a.nlines,k)+0.1*np.random.default_rng(0).normal(size=a.nlines),res[sh][key],"o")
    ax[j].set_xticks([0,1]); ax[j].set_xticklabels(["Chair44 line","shuffled"]); ax[j].set_title(lab,fontsize=9)
  ax[2].set_yscale("symlog",linthresh=1)
  fig.suptitle("%s lines, depth %d, strength %.2f" % (a.line,a.depth,a.lam),fontsize=9)
  finish(fig)
else:
  sys.exit("unknown task " + a.task)
