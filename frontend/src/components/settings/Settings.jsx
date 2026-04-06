import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Plus, Trash2 } from "lucide-react";
import { API_URL } from "@/config";

export default function Settings() {
  const [filterSets, setFilterSets] = useState([]);
  const [newSetName, setNewSetName] = useState("");
  const [newWordsBySet, setNewWordsBySet] = useState({});
  const [searchTermsBySet, setSearchTermsBySet] = useState({});
  const [audioBufferSeconds, setAudioBufferSeconds] = useState("0");
  const [isSavingBuffer, setIsSavingBuffer] = useState(false);
  const SETTINGS_URL = `${API_URL}/settings`;

  useEffect(() => {
    let isMounted = true;

    async function loadInitialSettings() {
      try {
        const [filterSetsRes, audioSettingsRes] = await Promise.all([
          fetch(`${SETTINGS_URL}/filter-sets`),
          fetch(`${SETTINGS_URL}/audio-processing`),
        ]);

        const filterSetsData = await filterSetsRes.json();
        const audioSettingsData = await audioSettingsRes.json();

        if (isMounted) {
          setFilterSets(filterSetsData.filter_sets || []);
          setAudioBufferSeconds(String(audioSettingsData.buffer_seconds ?? 0));
        }
      } catch (err) {
        console.error("Error loading settings:", err);
      }
    }

    loadInitialSettings();

    return () => {
      isMounted = false;
    };
  }, [SETTINGS_URL]);

  async function handleCreateSet() {
    const trimmedName = newSetName.trim();
    if (!trimmedName) return;

    try {
      const res = await fetch(`${SETTINGS_URL}/filter-sets`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: trimmedName }),
      });
      const data = await res.json();
      setFilterSets(data.filter_sets || []);
      setNewSetName("");
    } catch (err) {
      console.error("Error creating filter set:", err);
    }
  }

  async function handleToggleSet(setId, enabled) {
    try {
      const res = await fetch(`${SETTINGS_URL}/filter-sets/${setId}/toggle`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ enabled }),
      });
      const data = await res.json();
      setFilterSets(data.filter_sets || []);
    } catch (err) {
      console.error("Error toggling filter set:", err);
    }
  }

  async function handleAddWord(setId) {
    const pendingWord = (newWordsBySet[setId] || "").trim().toLowerCase();
    if (!pendingWord) return;

    try {
      const res = await fetch(`${SETTINGS_URL}/filter-sets/${setId}/add-word`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ word: pendingWord }),
      });
      const data = await res.json();
      setFilterSets(data.filter_sets || []);
      setNewWordsBySet((prev) => ({ ...prev, [setId]: "" }));
    } catch (err) {
      console.error("Error adding word to set:", err);
    }
  }

  async function handleRemoveWord(setId, word) {
    try {
      const res = await fetch(`${SETTINGS_URL}/filter-sets/${setId}/remove-word`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ word }),
      });
      const data = await res.json();
      setFilterSets(data.filter_sets || []);
    } catch (err) {
      console.error("Error removing word from set:", err);
    }
  }

  async function handleDeleteSet(setId) {
    try {
      const res = await fetch(`${SETTINGS_URL}/filter-sets/${setId}`, {
        method: "DELETE",
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to delete filter set");
      }

      setFilterSets(data.filter_sets || []);
      setNewWordsBySet((prev) => {
        const next = { ...prev };
        delete next[setId];
        return next;
      });
      setSearchTermsBySet((prev) => {
        const next = { ...prev };
        delete next[setId];
        return next;
      });
    } catch (err) {
      console.error("Error deleting filter set:", err);
    }
  }

  async function handleSaveAudioBuffer() {
    const parsedBuffer = Number(audioBufferSeconds);
    if (Number.isNaN(parsedBuffer) || parsedBuffer < 0) return;

    try {
      setIsSavingBuffer(true);
      const res = await fetch(`${SETTINGS_URL}/audio-processing`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ buffer_seconds: parsedBuffer }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to save audio buffer setting");
      }

      setAudioBufferSeconds(String(data.buffer_seconds ?? parsedBuffer));
    } catch (err) {
      console.error("Error updating audio buffer setting:", err);
    } finally {
      setIsSavingBuffer(false);
    }
  }

  return (
    <div className="space-y-4">
      <Card className="shadow-none">
        <CardHeader>
          <CardTitle>Audio Processing</CardTitle>
          <CardDescription>
            Configure processing delay around detected words.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <p className="text-sm font-medium">Buffer (seconds)</p>
          <div className="flex gap-2">
            <Input
              type="number"
              min="0"
              step="0.05"
              value={audioBufferSeconds}
              onChange={(e) => setAudioBufferSeconds(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSaveAudioBuffer();
              }}
              placeholder="0.0"
            />
            <Button onClick={handleSaveAudioBuffer} disabled={isSavingBuffer}>
              {isSavingBuffer ? "Saving..." : "Save"}
            </Button>
          </div>
          <p className="text-xs text-muted-foreground">
            Adds extra time before and after flagged words when muting/bleeping audio.
          </p>
        </CardContent>
      </Card>

      <Card className="shadow-none">
        <CardHeader>
          <CardTitle>Filter Sets</CardTitle>
          <CardDescription>
            Group filter words into sets, then enable or disable each set.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
          <Input
            value={newSetName}
            onChange={(e) => setNewSetName(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleCreateSet();
            }}
            placeholder="New filter set name"
          />
          <Button onClick={handleCreateSet} className="gap-1.5">
            <Plus className="w-4 h-4" />
            Add Set
          </Button>
        </div>

        <div className="space-y-3">
          {filterSets.map((filterSet) => {
            const setWords = filterSet.words || [];
            const query = (searchTermsBySet[filterSet.id] || "").trim().toLowerCase();
            const visibleWords = query
              ? setWords.filter((w) => w.toLowerCase().includes(query))
              : setWords;

            return (
              <details
                key={filterSet.id}
                className="rounded-md border bg-card"
                open
              >
                <summary className="cursor-pointer list-none px-4 py-3">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="space-y-1">
                      <p className="font-medium">{filterSet.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {setWords.length} words
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        className="gap-1.5"
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          handleDeleteSet(filterSet.id);
                        }}
                      >
                        <Trash2 className="w-4 h-4" />
                        Delete
                      </Button>
                      <label className="flex items-center gap-2 text-sm">
                        <span>Enabled</span>
                        <Switch
                          checked={!!filterSet.enabled}
                          onCheckedChange={(checked) =>
                            handleToggleSet(filterSet.id, checked)
                          }
                        />
                      </label>
                    </div>
                  </div>
                </summary>

                <div className="space-y-3 border-t px-4 py-3">
                  <Input
                    value={searchTermsBySet[filterSet.id] || ""}
                    onChange={(e) =>
                      setSearchTermsBySet((prev) => ({
                        ...prev,
                        [filterSet.id]: e.target.value,
                      }))
                    }
                    placeholder="Search words in this set..."
                  />

                  <div className="flex gap-2">
                    <Input
                      value={newWordsBySet[filterSet.id] || ""}
                      onChange={(e) =>
                        setNewWordsBySet((prev) => ({
                          ...prev,
                          [filterSet.id]: e.target.value,
                        }))
                      }
                      onKeyDown={(e) => {
                        if (e.key === "Enter") handleAddWord(filterSet.id);
                      }}
                      placeholder="Add word to this set"
                    />
                    <Button
                      onClick={() => handleAddWord(filterSet.id)}
                      className="gap-1.5"
                    >
                      <Plus className="w-4 h-4" />
                      Add
                    </Button>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {visibleWords.map((word, index) => (
                      <Badge
                        key={`${filterSet.id}-${word}-${index}`}
                        variant="secondary"
                        className="flex items-center gap-1"
                      >
                        {word}
                        <button
                          type="button"
                          onClick={() => handleRemoveWord(filterSet.id, word)}
                          className="ml-1 text-xs hover:text-red-500"
                          aria-label={`Remove ${word}`}
                        >
                          x
                        </button>
                      </Badge>
                    ))}

                    {visibleWords.length === 0 && (
                      <p className="text-sm text-muted-foreground">
                        No matching words in this set.
                      </p>
                    )}
                  </div>
                </div>
              </details>
            );
          })}

          {filterSets.length === 0 && (
            <p className="text-sm text-muted-foreground">
              No filter sets yet. Add your first set above.
            </p>
          )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
