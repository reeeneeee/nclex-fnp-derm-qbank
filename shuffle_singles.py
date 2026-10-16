import re, glob, random
random.seed(90)
targets=[]
def remap_refs(text, m):
    sub=lambda s: re.sub(r'\b[A-D]\b', lambda x: m[x.group()], s)
    text=re.sub(r'\((?:[A-D](?:, | and | or |/)?)+\)', lambda x: sub(x.group()), text)
    text=re.sub(r'\b(Options?|Choices?|answers?) ([A-D])((?:(?:, | and | or )[A-D])*)\b', lambda x: sub(x.group()), text)
    text=re.sub(r'\b([A-D])( is| and| or| are)\b', lambda x: m[x.group(1)]+x.group(2), text)
    return text
for p in sorted(glob.glob('parts/*.md')):
    blocks=open(p).read().strip().split('\n---\n')
    out=[]
    for b in blocks:
        if '[Single]' in b:
            lines=b.strip('\n').split('\n')
            oi=[i for i,l in enumerate(lines) if re.match(r'^[A-D]\. ',l)]
            ai=[i for i,l in enumerate(lines) if l.startswith('**Answer:**')][0]
            ans=lines[ai].split('**Answer:**')[1].strip()
            opts={lines[i][0]:lines[i][3:] for i in oi}
            assert len(opts)==4 and ans in opts, (p,b[:60])
            if not targets: targets=list('ABCD')*1; random.shuffle(targets)
            tgt=targets.pop()
            others=[k for k in 'ABCD' if k!=ans]; random.shuffle(others)
            newpos=[k for k in 'ABCD' if k!=tgt]
            m={ans:tgt, **dict(zip(others,newpos))}
            inv={v:k for k,v in m.items()}
            for j,i in enumerate(oi): L='ABCD'[j]; lines[i]=f"{L}. {opts[inv[L]]}"
            lines[ai]=f"**Answer:** {tgt}"
            ri=[i for i,l in enumerate(lines) if l.startswith('**Rationale:**')][0]
            lines[ri]=remap_refs(lines[ri], m)
            b='\n'.join(lines)
        out.append(b.strip('\n'))
    open(p,'w').write('\n\n---\n\n'.join(out)+'\n\n---\n')
