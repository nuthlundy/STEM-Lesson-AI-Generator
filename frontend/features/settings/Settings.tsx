import { useState } from "react";
import { Key, Save, BrainCircuit, User, Building, Settings2, ShieldCheck, CheckCircle2 } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";

type AIMode = "smart" | "personal" | "organization" | "offline";

export function Settings() {
  const [aiMode, setAiMode] = useState<AIMode>("smart");
  const [isAutoSelectEnabled, setIsAutoSelectEnabled] = useState(true);

  return (
    <div className="flex flex-col gap-6 max-w-4xl">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings2 className="h-5 w-5" />
            AI Provider Manager
          </CardTitle>
          <CardDescription>
            Configure how STEM Lesson AI processes your documents. Choose between automatic, personal, or organizational AI accounts.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <RadioGroup defaultValue="smart" onValueChange={(v) => setAiMode(v as AIMode)}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              
              {/* Smart Free AI */}
              <div className="relative">
                <RadioGroupItem value="smart" id="smart" className="peer sr-only" />
                <Label
                  htmlFor="smart"
                  className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary cursor-pointer"
                >
                  <div className="flex w-full items-center justify-between mb-2">
                    <BrainCircuit className="h-6 w-6" />
                    <Badge variant="secondary">Default</Badge>
                  </div>
                  <div className="flex w-full flex-col">
                    <span className="font-semibold text-base mb-1">Smart Free AI</span>
                    <span className="text-sm font-normal text-muted-foreground leading-snug">
                      Automatically selects the best free model for your STEM document. No API key required.
                    </span>
                  </div>
                </Label>
              </div>

              {/* Personal AI */}
              <div className="relative">
                <RadioGroupItem value="personal" id="personal" className="peer sr-only" />
                <Label
                  htmlFor="personal"
                  className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary cursor-pointer"
                >
                  <div className="flex w-full items-center justify-between mb-2">
                    <User className="h-6 w-6" />
                  </div>
                  <div className="flex w-full flex-col">
                    <span className="font-semibold text-base mb-1">Personal AI</span>
                    <span className="text-sm font-normal text-muted-foreground leading-snug">
                      Use your own API key for Gemini, OpenAI, Anthropic, or OpenRouter.
                    </span>
                  </div>
                </Label>
              </div>

              {/* Organization AI */}
              <div className="relative">
                <RadioGroupItem value="organization" id="organization" className="peer sr-only" />
                <Label
                  htmlFor="organization"
                  className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary cursor-pointer"
                >
                  <div className="flex w-full items-center justify-between mb-2">
                    <Building className="h-6 w-6" />
                  </div>
                  <div className="flex w-full flex-col">
                    <span className="font-semibold text-base mb-1">Organization AI</span>
                    <span className="text-sm font-normal text-muted-foreground leading-snug">
                      Managed by your school administrator. Uses pooled quotas and models.
                    </span>
                  </div>
                </Label>
              </div>

              {/* Offline AI */}
              <div className="relative">
                <RadioGroupItem value="offline" id="offline" className="peer sr-only" disabled />
                <Label
                  htmlFor="offline"
                  className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 opacity-50 cursor-not-allowed"
                >
                  <div className="flex w-full items-center justify-between mb-2">
                    <ShieldCheck className="h-6 w-6" />
                    <Badge variant="outline">Coming Soon</Badge>
                  </div>
                  <div className="flex w-full flex-col">
                    <span className="font-semibold text-base mb-1">Offline AI</span>
                    <span className="text-sm font-normal text-muted-foreground leading-snug">
                      Run models locally using Ollama or LM Studio. Total privacy.
                    </span>
                  </div>
                </Label>
              </div>
            </div>
          </RadioGroup>

          {/* Configuration Panels */}
          <div className="mt-8 pt-6 border-t">
            {aiMode === "smart" && (
              <div className="space-y-4 animate-in fade-in slide-in-from-top-2">
                <h3 className="text-lg font-medium">Smart Free Configuration</h3>
                
                <div className="flex items-center justify-between rounded-lg border p-4">
                  <div className="space-y-0.5">
                    <Label className="text-base">Auto Select Best Model</Label>
                    <p className="text-sm text-muted-foreground">
                      Platform will automatically route to Gemini Flash, DeepSeek, or Llama based on availability.
                    </p>
                  </div>
                  <Switch 
                    checked={isAutoSelectEnabled}
                    onCheckedChange={setIsAutoSelectEnabled}
                  />
                </div>

                {!isAutoSelectEnabled && (
                  <div className="space-y-2">
                    <Label>Preferred Free Provider</Label>
                    <Select defaultValue="openrouter">
                      <SelectTrigger>
                        <SelectValue placeholder="Select provider" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="openrouter">OpenRouter (Multiple Free Models)</SelectItem>
                        <SelectItem value="gemini">Google Gemini (Free Tier)</SelectItem>
                        <SelectItem value="groq">Groq (Fast Inference)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                )}
              </div>
            )}

            {aiMode === "personal" && (
              <div className="space-y-4 animate-in fade-in slide-in-from-top-2">
                <h3 className="text-lg font-medium">Personal API Key</h3>
                
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label>Provider</Label>
                    <Select defaultValue="gemini">
                      <SelectTrigger>
                        <SelectValue placeholder="Select provider" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="gemini">Google Gemini</SelectItem>
                        <SelectItem value="openai">OpenAI</SelectItem>
                        <SelectItem value="anthropic">Anthropic</SelectItem>
                        <SelectItem value="openrouter">OpenRouter</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <Label>Model</Label>
                    <Select defaultValue="gemini-1.5-pro">
                      <SelectTrigger>
                        <SelectValue placeholder="Select model" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="gemini-1.5-pro">Gemini 1.5 Pro</SelectItem>
                        <SelectItem value="gemini-1.5-flash">Gemini 1.5 Flash</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="api-key">API Key</Label>
                  <div className="flex gap-2">
                    <Input 
                      id="api-key" 
                      type="password" 
                      placeholder="Enter your API key..." 
                      defaultValue="AIzaSy..."
                    />
                    <Button variant="secondary">Validate</Button>
                  </div>
                  <div className="flex items-center gap-1 mt-2 text-sm text-green-600 dark:text-green-400">
                    <CheckCircle2 className="h-4 w-4" />
                    <span>Connected and verified</span>
                  </div>
                </div>
              </div>
            )}

            {aiMode === "organization" && (
              <div className="space-y-4 animate-in fade-in slide-in-from-top-2">
                <h3 className="text-lg font-medium">Organization Managed</h3>
                
                <div className="rounded-lg border p-4 bg-muted/50">
                  <div className="space-y-3">
                    <div>
                      <Label className="text-muted-foreground">Organization</Label>
                      <p className="font-medium mt-1">Western International School</p>
                    </div>
                    <div>
                      <Label className="text-muted-foreground">Assigned Model</Label>
                      <p className="font-medium mt-1">OpenAI GPT-4o (Managed)</p>
                    </div>
                    <div className="flex items-center gap-2 mt-4 text-sm text-muted-foreground bg-background rounded p-2 border">
                      <Building className="h-4 w-4" />
                      <span>This configuration is managed by your school administrator.</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </CardContent>
        <CardFooter className="border-t px-6 py-4">
          <Button className="ml-auto">
            <Save className="mr-2 h-4 w-4" />
            Save Configuration
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
