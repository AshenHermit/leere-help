import React from "react"
import { Button } from "../components/ui/button"
import { Input } from "@/components/ui/input"
import { useApiRequest } from "./utils"

function ValueInput({
  value,
  onValueChange,
  ...props
}: React.ComponentProps<typeof Input> & { onValueChange: (value: string) => void }) {
  return (
    <Input
      value={value}
      className="bg-slate-950 p-2"
      onChangeCapture={(e) => onValueChange(e.currentTarget.value)}
      {...props}
    />
  )
}

function App() {
  const userInfo = React.useState()

  return (
    <AppContainer>
      <div className="text-foreground flex h-full min-h-screen w-full items-center justify-center gap-4">
        <AppBlock>
          <AuthBlock />
        </AppBlock>
        <AppBlock></AppBlock>
        <AppBlock></AppBlock>
      </div>
    </AppContainer>
  )
}

function AuthBlock() {
  const [login, setLogin] = React.useState("")
  const [password, setPassword] = React.useState("")

  const { error, request, result } = useApiRequest()

  const auth = React.useCallback(async () => {
    await request("/", {})
  }, [request])

  return (
    <>
      <div className="text-foreground text-center">авторизация {login}</div>

      <div>login</div>
      <ValueInput value={login} placeholder="login" onValueChange={setLogin} />
      <div>password</div>
      <ValueInput
        value={password}
        type="password"
        placeholder="password"
        onValueChange={setPassword}
      />
      <Button className="bg-primary" onClick={auth}>
        Auth
      </Button>
    </>
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
    <div className="flex h-full min-h-screen w-full items-center justify-center gap-4 bg-zinc-950">
      {children}
    </div>
  )
}

export default App
