import { useCallback } from "react";
import { useSessionContext } from '@supabase/auth-helpers-react';
import { BACKEND_URL } from "../constants";

type Opts = Parameters<typeof fetch>[1];

export const useRequestCallback = (route: string, opts?: Opts) => {
  const { session } = useSessionContext();
  const makeRequest = useCallback(async () => {
    const { headers, ...rest } = opts || {};

    const res = await fetch(`${BACKEND_URL}${route}`, {
      ...rest,
      headers: {
        Authorization: `Bearer ${session?.access_token}`,
        ...headers,
      }
    });
    return res.json();
  }, [route, opts, session?.access_token]);


  return makeRequest;
}
