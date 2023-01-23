import {
  useSessionContext,
  useSupabaseClient,
  useUser
} from '@supabase/auth-helpers-react';
import { useRouter } from 'next/router';
import { Auth, ThemeSupa } from '@supabase/auth-ui-react';
import type { NextPage } from 'next';
import Link from 'next/link';
import Feed from '@/components/Feed';
import { useEffect, useState } from 'react';

const LoginPage: NextPage = () => {
  const { isLoading, session, error } = useSessionContext();
  const user = useUser();
  const supabaseClient = useSupabaseClient();
  const router = useRouter();

  const [data, setData] = useState(null);

  useEffect(() => {
    async function loadData() {
      const { data } = await supabaseClient.from('users').select('*').single();
      setData(data);
    }

    if (user) loadData();
  }, [user, supabaseClient]);

  useEffect(() => {
    const timeout = setInterval(() => {
      supabaseClient.auth.refreshSession()
    }, 5 * 60 * 1000);
    return () => {
      clearInterval(timeout);
    }
  }, [user, supabaseClient]);

  if (!session)
    return (
      <div className="w-screen h-screen">
        <Auth
          redirectTo={process.env.HOST}
          appearance={{ theme: ThemeSupa }}
          supabaseClient={supabaseClient}
          providers={['twitter']}
          socialLayout="horizontal"
          // onlyThirdPartyProviders
        />
      </div>
    );

  return (
    <div className="w-screen h-screen bg-[#15202b] text-white">
      <button
        onClick={async () => {
          await supabaseClient.auth.signOut();
          router.push('/');
        }}
      >
        Logout
      </button>
      <Feed />
    </div>
  );
};

export default LoginPage;
