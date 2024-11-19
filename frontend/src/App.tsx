import React from "react"
import "./App.css"
import { Button } from "./components/ui/button"

function App() {
  return (
    <>
      <div className="flex items-center justify-center">
        <div className="min-h-[200px] w-full bg-gray-800 sm:min-w-[200px]">
          <div className="text-foreground">lol</div>
          <Button className="bg-primary">shadcn</Button>
        </div>
      </div>
    </>
  )
}

export default App
