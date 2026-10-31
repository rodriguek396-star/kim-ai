import type {CSSProperties} from 'react';
/** Orb d'état inspiré des Thinking Orbs communautaires 21st.dev, recréé sans dépendance WebGL. */
export function Orb({size=48,state='idle'}:{size?:number;state?:'idle'|'thinking'|'speaking'}){return <span className={`orb orb-${state}`} style={{'--orb-size':`${size}px`} as CSSProperties} aria-label={state==='thinking'?'Kim réfléchit':'Kim est disponible'}><span/><i/><b/></span>}
