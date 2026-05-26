import React, { useEffect, useRef } from 'react';

export function DynamicBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = window.innerWidth;
    let height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;

    const handleResize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width;
      canvas.height = height;
    };
    window.addEventListener('resize', handleResize);

    const mouse = { x: width / 2, y: height / 2, radius: 250 };
    const targetMouse = { x: width / 2, y: height / 2 };

    const handleMouseMove = (e: MouseEvent) => {
      targetMouse.x = e.clientX;
      targetMouse.y = e.clientY;
    };
    window.addEventListener('mousemove', handleMouseMove);

    // Particle Setup (Hyperspace/Forward motion)
    const numParticles = 1200;
    const particles: any[] = [];
    
    for (let i = 0; i < numParticles; i++) {
      particles.push({
        baseX: (Math.random() - 0.5) * (width * 2),
        baseY: (Math.random() - 0.5) * (height * 2),
        baseZ: (Math.random() - 0.5) * 1600, // Deep depth
        size: Math.random() * 1.5 + 1,
        type: Math.random(),
        // Speed moving towards camera (Z-axis)
        vz: Math.random() * 2.5 + 1.5,
      });
    }

    let animationFrameId: number;

    const render = () => {
      ctx.clearRect(0, 0, width, height);
      
      // Smooth mouse interpolation
      mouse.x += (targetMouse.x - mouse.x) * 0.08;
      mouse.y += (targetMouse.y - mouse.y) * 0.08;

      const cx = width / 2;
      const cy = height / 2;

      // Dark Mode Colors only
      const cPrimary = '#60a5fa'; // Bright blue
      const cSecondary = '#e2e8f0'; // Off-white
      const cAccent = '#fde047'; // Bright Gold

      particles.forEach(p => {
        // Move towards the camera (decreasing Z)
        p.baseZ -= p.vz;

        // Wrap around to the back if they pass the camera plane (-perspective)
        if (p.baseZ < -900) {
          p.baseZ = 900;
          p.baseX = (Math.random() - 0.5) * (width * 2);
          p.baseY = (Math.random() - 0.5) * (height * 2);
        }

        // Base coordinates relative to center
        let rx = p.baseX;
        let ry = p.baseY;
        let rz = p.baseZ;

        // Perspective Projection
        const perspective = 900;
        const scale = perspective / (perspective + rz);
        const px = cx + rx * scale;
        const py = cy + ry * scale;

        // Mouse Repulsion (Interactive)
        const dx = mouse.x - px;
        const dy = mouse.y - py;
        const dist = Math.sqrt(dx * dx + dy * dy);

        let pushX = 0;
        let pushY = 0;

        if (dist < mouse.radius) {
          const force = Math.pow((mouse.radius - dist) / mouse.radius, 2);
          pushX = -(dx / dist) * force * 150;
          pushY = -(dy / dist) * force * 150;
        }

        const finalScale = perspective / (perspective + rz);
        const screenX = cx + (rx + pushX) * finalScale;
        const screenY = cy + (ry + pushY) * finalScale;

        // Render particle if in front of the camera
        if (rz > -perspective) {
          // Fade based on depth
          const zAlpha = Math.max(0.05, Math.min(1, (rz + 450) / 900));
          
          ctx.beginPath();
          ctx.arc(screenX, screenY, p.size * finalScale, 0, Math.PI * 2);
          
          let fill = cPrimary;
          if (p.type < 0.15) fill = cAccent;
          else if (p.type < 0.45) fill = cSecondary;

          ctx.fillStyle = fill;
          ctx.globalAlpha = zAlpha;
          ctx.fill();
        }
      });
      
      ctx.globalAlpha = 1;
      animationFrameId = requestAnimationFrame(render);
    };
    
    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 transition-colors duration-500">
      {/* Dynamic ambient color blobs (Aurora effect) */}
      <div 
        className="absolute w-[60vw] h-[60vw] rounded-full mix-blend-normal opacity-40 blur-[100px] md:blur-[140px]" 
        style={{
          backgroundColor: 'var(--primary-color)',
          top: '10%',
          left: '20%',
          animation: 'float-blob-1 25s infinite alternate ease-in-out',
        }}
      />
      <div 
        className="absolute w-[50vw] h-[50vw] rounded-full mix-blend-normal opacity-40 blur-[100px] md:blur-[140px]" 
        style={{
          backgroundColor: 'var(--gold-color)',
          bottom: '10%',
          right: '10%',
          animation: 'float-blob-2 30s infinite alternate ease-in-out',
        }}
      />

      {/* 3D Particle Canvas */}
      <canvas 
        ref={canvasRef} 
        className="absolute inset-0 w-full h-full z-10"
      />
    </div>
  );
}
