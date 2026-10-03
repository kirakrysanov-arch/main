import subprocess, os
from brands import concept, proposal
from brand_data import BRANDS
S='/tmp/claude-0/-home-user-main/8841ce66-6ddd-5dbc-87d4-373a29e45e36/scratchpad/'
env=dict(os.environ, NODE_PATH='/opt/node22/lib/node_modules')
OUT={'mirror':'Mirror','express':'Express','men':'MEN'}
for B in BRANDS:
    k=B['key']; nm=OUT[k]
    open(f'{k}-concept.html','w').write(concept(B))
    subprocess.run(['node','render.js',f'{k}-concept.html',f'../reach-brands/reChanneld-{nm}-Concept.pdf','long',S+f'{k}-c.png'],env=env,check=True)
    subprocess.run(['convert',S+f'{k}-c.png','-resize','700x','-quality','88',f'img/b/{k}-cfull.jpg'],check=True)
    subprocess.run(['node','shot.js',f'{k}-concept.html','.browser','1',f'img/b/{k}-scene2.jpg'],env=env,check=True)
    subprocess.run(['node','shot.js',f'{k}-concept.html','#s3','0',f'img/b/{k}-scene3.jpg'],env=env,check=True)
    open(f'{k}-proposal.html','w').write(proposal(B))
    subprocess.run(['node','render.js',f'{k}-proposal.html',f'../reach-brands/reChanneld-for-{nm}.pdf','a4'],env=env,check=True)
    print('done',k)
