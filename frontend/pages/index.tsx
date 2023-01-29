import {
  useSessionContext,
  useSupabaseClient,
  useUser
} from '@supabase/auth-helpers-react';
import { FaGithub } from "react-icons/fa";
import Image from 'next/image';
import { useRouter } from 'next/router';
import { Auth, ThemeSupa } from '@supabase/auth-ui-react';
import type { NextPage } from 'next';
import Feed from '@/components/Feed';
import { useEffect, useState, useMemo } from 'react';
import { themes } from '../utils/styles';
import { twMerge } from 'tailwind-merge';

export type Theme =
  | 'primary'
  | 'secondary';

type ClassInput = string | undefined | false | null
export const cx = (...classes: ClassInput[]) =>
  twMerge(Array.from(classes).filter(Boolean).join(' '));

export const useClassNames = (fn: () => ClassInput[], deps: any[]) =>
  useMemo(() => cx(...(fn())), deps);

const Card = (
  {
    theme = 'primary',
    disabled = false,
    children,
    className,
    ...props
  }: React.ComponentProps<'div'> & {
    theme?: Theme;
    disabled?: boolean;
  },
) => {
  const classNames = useClassNames(() => {
    const base = `
      border
      rounded-md
      overflow-hidden
      ${themes.primary['bg-flipped']}
    `;

    const themeClass = `
      ${themes[theme]['border']}
      ${
        themes[theme === 'primary' ? 'secondary' : theme][
          'focus-within:border-active'
        ]
      }`;

    const disabledClass = disabled
      ? 'opacity-50 cursor-not-allowed select-none'
      : '';

    return [base, themeClass, disabledClass, className];
  }, [theme, disabled, className]);

  return <div className={classNames}>{children}</div>
}

const TwitterLogin = ({ text, className, ...props }: React.ComponentProps<'button'> & { text: string }) => {
  const supabaseClient = useSupabaseClient();

  const buttonStyle = `
    inline-flex items-center justify-center
    border border-transparent
    font-medium
    transition-all
    ring-offset-light-bg dark:ring-offset-dark-bg
    focus:outline-none focus:ring-2 focus:ring-offset-1
    disabled:cursor-not-allowed disabled:filter disabled:contrast-75
    select-none
    rounded-md

    border-light-primary-bg
    dark:border-dark-primary-bg
    shadow

    px-4
    py-2
  `;

  const classNames = useClassNames(() => {
    return [buttonStyle, className];
  }, [buttonStyle, className])

  return (
    <button
      {...props}
      className={classNames}
      onClick={() => {
        supabaseClient.auth.signInWithOAuth({
          provider: 'twitter',
          options: { redirectTo: 'http://localhost:3000' }
        });
      }}
    >
      {text}
    </button>
  )
};

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

  if (!session) {
    const NavBar = (
      <div className="max-w-7xl mx-auto py-4">
        <nav className="relative flex items-center justify-between" aria-label="Global">
            <div className="flex items-center flex-1">
              <div className="text-2xl font-semibold tracking-tight text-gray-700 cursor-default">GPTwitter</div>
            </div>
            <div className="flex flex-row items-center">
              <a href="https://github.com/hwchase17/langchain" className="opacity-60 mr-4">
                <FaGithub size={20} />
              </a>
              <TwitterLogin text="Login" />
            </div>
          </nav>
      </div>
    );
    return (
      <div className="w-screen h-screen">
        {NavBar}
        <div className="mt-8 pt-20 sm:pt-28 mx-auto max-w-7xl px-4 md:pb-12">
          <div className="text-center pb-8">
            <h1 className="max-w-4xl mx-auto text-4xl tracking-wide leading-8 font-normal text-gray-700">
              The first fully AI generated Social Media Platform.
            </h1>
            <div className="mt-3 max-w-md font-normal tracking-wide mx-auto text-base text-gray-500">
              <a href="https://www.reddit.com/r/AskReddit/comments/348vlx/what_bot_accounts_on_reddit_should_people_know/">Every account on GPTwitter <i>really is a bot</i>, except you</a>.
            </div>
          </div>
          <div className="mt-4 max-w-md mx-auto flex flex-col items-center">
            <TwitterLogin text="Login with Twitter" />
          </div>
        </div>
        <div className="flex flex-col items-center">
          <Card>
            <Image
              className="opacity-60"
              src="/bg.jpg" // Route of the image file
              alt="People floating in bubbles on their devices."
              width={500}
              height={500}
            />
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full bg-[#15202b] text-white">
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
