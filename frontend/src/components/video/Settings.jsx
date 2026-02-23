import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export default function Settings() {
  const [filterWords, setFilterWords] = useState([]);
  const [newWord, setNewWord] = useState("");
  const API_URL = "http://localhost:8000/settings";

  async function handleAddWord() {
  const trimmed = newWord.trim().toLowerCase();
  if (!trimmed) return;

  try {
    const res = await fetch("http://localhost:8000/settings/add-word", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ word: trimmed }),
    });

    const data = await res.json();

    // Update UI with backend response
    setFilterWords(data.words || []);
    setNewWord("");
  } catch (err) {
    console.error("Error sending word to backend:", err);
  }
}
  
  return (
    <div className="space-y-4">
        <div>
          <h3 className="text-lg font-semibold">Word Filter</h3>
          <p className="text-sm text-muted-foreground">
            Add words you want automatically filtered.
          </p>
        </div>

        <div className="flex gap-2">
          <Input
            value={newWord}
            onChange={(e) => setNewWord(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleAddWord();
            }}
            placeholder="Enter word"
          />
          <Button onClick={handleAddWord}>
            Add
          </Button>
        </div>

        <div className="flex flex-wrap gap-2">
          {filterWords.map((word, index) => (
            <Badge key={index} variant="secondary">
              {word}
            </Badge>
          ))}
        </div>
    </div>
  );
}
