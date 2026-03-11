import { useEffect, useMemo, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export default function Settings() {
  const [filterWords, setFilterWords] = useState([]);
  const [newWord, setNewWord] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
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

  async function loadWords() {
    try {
      const res = await fetch(`${API_URL}/words`);
      const data = await res.json();
      setFilterWords(data.words || []);
    } catch (err) {
      console.error("Error loading words:", err);
    }
  }

  useEffect(() => {
    loadWords();
  }, []);

async function handleRemoveWord(word) {
  try {
    const res = await fetch("http://localhost:8000/settings/remove-word", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ word }),
    });

    const data = await res.json();

    setFilterWords(data.words || []);
  } catch (err) {
    console.error("Error removing word:", err);
  }
}

const visibleWords = useMemo(() => {
    const q = searchTerm.trim().toLowerCase();
    if (!q) return filterWords;
    return filterWords.filter((w) => w.toLowerCase().includes(q));
  }, [filterWords, searchTerm]);

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

        <Input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search words..."
              />

        <div className="flex flex-wrap gap-2">
        {visibleWords.map((word, index) => (
          <Badge
            key={`${word}-${index}`}
            variant="secondary"
            className="flex items-center gap-1"
          >
            {word}
            <button
              type="button"
              onClick={() => handleRemoveWord(word)}
              className="ml-1 text-xs hover:text-red-500"
              aria-label={`Remove ${word}`}
            >
              ✕
            </button>
          </Badge>
        ))}

        {/* Optional: empty state */}
        {visibleWords.length === 0 && (
          <p className="text-sm text-muted-foreground">No matching words.</p>
        )}
      </div>
    </div>
  );
}
