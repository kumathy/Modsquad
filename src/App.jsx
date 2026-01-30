import { useState } from 'react';

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function App() {
  
  return (
    <div className="p-6">
      <Card>
        <h2>Welcome to ModSquad</h2>
        <Button>Launch</Button>
      </Card>
    </div>
  )
}
