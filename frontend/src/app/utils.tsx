import React from "react"

export const API_PATH = "localhost:8000/api/"

export type UserInfo = {
  name: string
  login: string
}

export async function makeApiRequest<T, D>(route: string, data: D) {
  var url = new URL(API_PATH + route)
  var rawData = data as { [key: string]: any }
  Object.keys(rawData).forEach((x) => url.searchParams.set(x, rawData[x]))

  var res = await fetch(url)
  var resData = await res.json()
  if (resData.error) throw new Error(resData.error)
  return resData.data as T
}

export function useApiRequest<T, D>() {
  const [resultData, setResultData] = React.useState<T | null>(null)
  const [error, setError] = React.useState<string | null>(null)

  const request = React.useCallback(async (route: string, data: D) => {
    try {
      setError(null)
      var res = await makeApiRequest<T, D>(route, data)
      setResultData(res)
      return res
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message)
      }
    }
    return null
  }, [])

  return { result: resultData, request: request, error: error }
}
