import { useState } from 'react';

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Separator } from '@/components/ui/separator';

export default function App() {
  
  return (
    <div className='min-h-screen'>
      <header className='border-b'>
        <div className="container mx-auto px-4 py-6">
          <h1 className='scroll-m-20 text-3xl font-bold tracking-tight text-balance'>Modsquad</h1>
          <p className='leading-7 text-muted-foreground'>
          Stream Moderation with AI-Powered Voice Cloning
          </p>
        </div>
      </header>
    </div>
  )
}
