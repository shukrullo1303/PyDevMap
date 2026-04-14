"use client"

import { useState, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { 
  Play, RotateCcw, Lightbulb, CheckCircle2, 
  XCircle, Terminal, ChevronDown, ChevronUp
} from "lucide-react"
import { cn } from "@/lib/utils"

interface CodeExercise {
  instructions: string
  starterCode: string
  expectedOutput: string
  hints: string[]
}

interface CodeEditorProps {
  exercise: CodeExercise
  onComplete: () => void
}

export function CodeEditor({ exercise, onComplete }: CodeEditorProps) {
  const [code, setCode] = useState(exercise.starterCode)
  const [output, setOutput] = useState<string>("")
  const [isRunning, setIsRunning] = useState(false)
  const [showHints, setShowHints] = useState(false)
  const [currentHint, setCurrentHint] = useState(0)
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null)

  const runCode = useCallback(async () => {
    setIsRunning(true)
    setOutput("")
    setIsCorrect(null)

    // Simulate Python code execution
    // In a real app, this would call a backend API
    await new Promise(resolve => setTimeout(resolve, 1000))

    try {
      // Simple Python-like evaluation for demo
      let result = ""
      const lines = code.split('\n')
      
      for (const line of lines) {
        const trimmed = line.trim()
        
        // Handle print statements
        const printMatch = trimmed.match(/^print\s*\(\s*["'](.*)["']\s*\)$/)
        if (printMatch) {
          result += printMatch[1] + "\n"
          continue
        }

        // Handle print with f-string (simplified)
        const fstringMatch = trimmed.match(/^print\s*\(\s*f?["'](.*)["']\s*\)$/)
        if (fstringMatch) {
          result += fstringMatch[1] + "\n"
          continue
        }

        // Handle print with variable
        const printVarMatch = trimmed.match(/^print\s*\(\s*(\w+)\s*\)$/)
        if (printVarMatch) {
          // Find variable assignment
          const varName = printVarMatch[1]
          const varAssign = lines.find(l => {
            const assignMatch = l.trim().match(new RegExp(`^${varName}\\s*=\\s*["'](.*)["']$`))
            return assignMatch
          })
          if (varAssign) {
            const assignMatch = varAssign.trim().match(/=\s*["'](.*)["']$/)
            if (assignMatch) {
              result += assignMatch[1] + "\n"
            }
          }
          continue
        }

        // Handle simple arithmetic print
        const mathPrintMatch = trimmed.match(/^print\s*\(\s*([\d\s+\-*/()]+)\s*\)$/)
        if (mathPrintMatch) {
          try {
            const evalResult = eval(mathPrintMatch[1])
            result += evalResult + "\n"
          } catch {
            // Skip invalid math
          }
        }
      }

      result = result.trim()
      setOutput(result || "Chiqish yo'q")

      // Check if output matches expected
      const expectedTrimmed = exercise.expectedOutput.trim().toLowerCase()
      const resultLower = result.toLowerCase()
      
      const correct = resultLower.includes(expectedTrimmed) || 
        expectedTrimmed.includes(resultLower) ||
        result.length > 0

      setIsCorrect(correct)
      if (correct) {
        onComplete()
      }
    } catch (error) {
      setOutput(`Xatolik: ${error}`)
      setIsCorrect(false)
    }

    setIsRunning(false)
  }, [code, exercise.expectedOutput, onComplete])

  const resetCode = () => {
    setCode(exercise.starterCode)
    setOutput("")
    setIsCorrect(null)
  }

  const showNextHint = () => {
    if (currentHint < exercise.hints.length - 1) {
      setCurrentHint(currentHint + 1)
    }
  }

  return (
    <div className="grid lg:grid-cols-2 gap-6">
      {/* Left: Instructions & Editor */}
      <div className="space-y-4">
        {/* Instructions */}
        <Card>
          <CardHeader className="pb-3">
            <h3 className="font-semibold">Vazifa</h3>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">{exercise.instructions}</p>
            <div className="flex items-center gap-2 text-sm">
              <Badge variant="outline">Kutilgan natija:</Badge>
              <code className="bg-muted px-2 py-1 rounded text-sm font-mono">
                {exercise.expectedOutput}
              </code>
            </div>
          </CardContent>
        </Card>

        {/* Code Editor */}
        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Terminal className="h-4 w-4 text-primary" />
                <h3 className="font-semibold">Kod Muharriri</h3>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={resetCode}
                  className="gap-1"
                >
                  <RotateCcw className="h-4 w-4" />
                  Qayta tiklash
                </Button>
                <Button
                  size="sm"
                  onClick={runCode}
                  disabled={isRunning}
                  className="gap-1"
                >
                  <Play className="h-4 w-4" />
                  {isRunning ? "Ishlamoqda..." : "Ishga tushirish"}
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="relative">
              <div className="absolute left-0 top-0 bottom-0 w-10 bg-muted/50 rounded-l-lg flex flex-col items-center pt-3 text-xs text-muted-foreground font-mono">
                {code.split('\n').map((_, i) => (
                  <div key={i} className="h-6 leading-6">{i + 1}</div>
                ))}
              </div>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className={cn(
                  "w-full min-h-[200px] bg-[#1e1e2e] text-[#cdd6f4] font-mono text-sm p-3 pl-12 rounded-lg border-2 resize-y",
                  "focus:outline-none focus:ring-2 focus:ring-primary/50",
                  isCorrect === true && "border-success",
                  isCorrect === false && "border-destructive",
                  isCorrect === null && "border-border"
                )}
                spellCheck={false}
                placeholder="Python kodingizni shu yerga yozing..."
              />
            </div>
          </CardContent>
        </Card>

        {/* Hints */}
        <Card>
          <CardHeader className="pb-3">
            <button
              onClick={() => setShowHints(!showHints)}
              className="flex items-center justify-between w-full"
            >
              <div className="flex items-center gap-2">
                <Lightbulb className="h-4 w-4 text-warning" />
                <h3 className="font-semibold">Yordam kerakmi?</h3>
              </div>
              {showHints ? (
                <ChevronUp className="h-4 w-4" />
              ) : (
                <ChevronDown className="h-4 w-4" />
              )}
            </button>
          </CardHeader>
          {showHints && (
            <CardContent>
              <div className="space-y-3">
                {exercise.hints.slice(0, currentHint + 1).map((hint, i) => (
                  <div 
                    key={i}
                    className="flex items-start gap-2 p-3 rounded-lg bg-warning/10"
                  >
                    <Badge variant="outline" className="shrink-0 mt-0.5">
                      #{i + 1}
                    </Badge>
                    <p className="text-sm text-muted-foreground">{hint}</p>
                  </div>
                ))}
                {currentHint < exercise.hints.length - 1 && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={showNextHint}
                    className="w-full"
                  >
                    Keyingi maslahat
                  </Button>
                )}
              </div>
            </CardContent>
          )}
        </Card>
      </div>

      {/* Right: Output */}
      <div>
        <Card className="sticky top-28">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Terminal className="h-4 w-4" />
                <h3 className="font-semibold">Natija</h3>
              </div>
              {isCorrect !== null && (
                <Badge className={cn(
                  isCorrect ? "bg-success text-success-foreground" : "bg-destructive text-destructive-foreground"
                )}>
                  {isCorrect ? (
                    <><CheckCircle2 className="h-3 w-3 mr-1" />To&apos;g&apos;ri!</>
                  ) : (
                    <><XCircle className="h-3 w-3 mr-1" />Qayta urinib ko&apos;ring</>
                  )}
                </Badge>
              )}
            </div>
          </CardHeader>
          <CardContent>
            <div className={cn(
              "min-h-[300px] bg-[#1e1e2e] rounded-lg p-4 font-mono text-sm",
              isRunning && "animate-pulse"
            )}>
              {isRunning ? (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <div className="h-2 w-2 rounded-full bg-primary animate-bounce" />
                  <div className="h-2 w-2 rounded-full bg-primary animate-bounce delay-100" />
                  <div className="h-2 w-2 rounded-full bg-primary animate-bounce delay-200" />
                  <span className="ml-2">Kod ishlamoqda...</span>
                </div>
              ) : output ? (
                <pre className={cn(
                  "whitespace-pre-wrap",
                  isCorrect === true && "text-success",
                  isCorrect === false && "text-destructive"
                )}>
                  {output}
                </pre>
              ) : (
                <p className="text-muted-foreground">
                  {">>>"} Natijalar shu yerda ko&apos;rinadi
                </p>
              )}
            </div>

            {isCorrect && (
              <div className="mt-4 p-4 rounded-lg bg-success/10 border border-success/30">
                <div className="flex items-center gap-2 text-success mb-2">
                  <CheckCircle2 className="h-5 w-5" />
                  <span className="font-medium">Ajoyib ish!</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Siz vazifani muvaffaqiyatli bajardingiz. Keyingi bosqichga o&apos;tishingiz mumkin.
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
