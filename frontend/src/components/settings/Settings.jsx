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
import { Plus, Trash2, RotateCcw, X, Search } from "lucide-react";
import { API_URL } from "@/config";

export default function Settings() {
  const [filterSets, setFilterSets] = useState([]);
  const [newSetName, setNewSetName] = useState("");
  const [newWordsBySet, setNewWordsBySet] = useState({});
  const [searchTermsBySet, setSearchTermsBySet] = useState({});
  const [audioBufferSeconds, setAudioBufferSeconds] = useState("0");
  const [isSavingBuffer, setIsSavingBuffer] = useState(false);
  const [censorWords, setCensorWords] = useState(true);
  const SETTINGS_URL = `${API_URL}/settings`;

  function censorWord(word) {
    if (!censorWords || word.length <= 2) return word;
    return word[0] + "*".repeat(word.length - 2) + word[word.length - 1];
  }

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

  async function handleResetSet(setId) {
    try {
      const res = await fetch(`${SETTINGS_URL}/filter-sets/${setId}/reset`, {
        method: "POST",
      });
      const data = await res.json();
      setFilterSets(data.filter_sets || []);
    } catch (err) {
      console.error("Error resetting filter set:", err);
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
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Filter Sets</CardTitle>
              <CardDescription>
                Group filter words into sets, then enable or disable each set.
              </CardDescription>
            </div>
            <label className="flex items-center gap-2 text-sm">
              <span>Censor words</span>
              <Switch
                checked={censorWords}
                onCheckedChange={setCensorWords}
              />
            </label>
          </div>
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
                <summary className="cursor-pointer list-none rounded-md px-4 py-3 transition-colors hover:bg-accent">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <Switch
                        checked={!!filterSet.enabled}
                        onCheckedChange={(checked) => {
                          handleToggleSet(filterSet.id, checked);
                        }}
                        onClick={(e) => e.stopPropagation()}
                      />
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <p className="font-medium">{filterSet.name}</p>
                          {filterSet.isDefault && <Badge variant="outline">Default</Badge>}
                        </div>
                        <p className="text-xs text-muted-foreground">
                          {setWords.length} words
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {filterSet.isDefault ? (
                        <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            className="gap-1.5 w-20 hover:bg-amber-100 hover:text-amber-700 hover:border-amber-300"
                            onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              handleResetSet(filterSet.id);
                            }}
                          >
                            <RotateCcw className="w-4 h-4" />
                            Reset
                          </Button>
                      ) : (
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          className="gap-1.5 w-20 hover:bg-red-100 hover:text-red-700 hover:border-red-300"
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            handleDeleteSet(filterSet.id);
                          }}
                        >
                          <Trash2 className="w-4 h-4" />
                          Delete
                        </Button>
                      )}
                    </div>
                  </div>
                </summary>

                <div className="space-y-3 border-t px-4 py-3">
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
                      placeholder="Add a word to this set..."
                    />
                    <Button
                      onClick={() => handleAddWord(filterSet.id)}
                      className="gap-1.5"
                    >
                      <Plus className="w-4 h-4" />
                      Add
                    </Button>
                  </div>

                  <div className="relative">
                    <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      className="pl-8"
                      value={searchTermsBySet[filterSet.id] || ""}
                      onChange={(e) =>
                        setSearchTermsBySet((prev) => ({
                          ...prev,
                          [filterSet.id]: e.target.value,
                        }))
                      }
                      placeholder="Search words..."
                    />
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {visibleWords.map((word, index) => (
                      <Badge
                        key={`${filterSet.id}-${word}-${index}`}
                        variant="secondary"
                        className="flex items-center gap-1 rounded-full border border-zinc-300"
                      >
                        {censorWord(word)}
                        <button
                          type="button"
                          onClick={() => handleRemoveWord(filterSet.id, word)}
                          className="ml-1 rounded-full p-0.5 text-xs hover:bg-red-100 hover:text-red-500"
                          aria-label={`Remove ${word}`}
                        >
                          <X className="w-3 h-3" />
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
