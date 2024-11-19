import React from "react"
import { Button } from "../components/ui/button"

function App() {
  return (
    <AppContainer>
      <div className="flex h-full min-h-screen w-full items-center justify-center gap-4">
        <AppBlock>
          <div className="text-foreground text-center">авторизация</div>
          <Button className="bg-primary">shadcn</Button>
        </AppBlock>
        <AppBlock></AppBlock>
      </div>
    </AppContainer>
  )
}

function AppBlock({ children }: React.PropsWithChildren<{}>) {
  return (
    <div className="flex min-h-[200px] w-full flex-col gap-4 rounded-xl bg-zinc-800 p-8 sm:w-auto sm:min-w-[200px]">
      {children}
    </div>
  )
}

function AppContainer({ children }: React.PropsWithChildren<{}>) {
  return (
    <div className="flex h-full min-h-screen w-full items-center justify-center gap-4">
      {children}
    </div>
  )
}

export default App
