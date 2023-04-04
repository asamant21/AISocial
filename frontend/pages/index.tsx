import {
  useSessionContext,
  useSupabaseClient,
  useUser
} from '@supabase/auth-helpers-react';
import { FaGithub, FaTwitter } from "react-icons/fa";
import Image from 'next/image';
import { useRouter } from 'next/router';
import type { NextPage } from 'next';
import Feed from '@/components/Feed';
import { useEffect, useState, useMemo } from 'react';
import { Oval } from "react-loader-spinner";
import { themes } from '../utils/styles';
import { twMerge } from 'tailwind-merge';
import { Center, Button, TextInput, Select, Stack, Space, Text, Title } from "@mantine/core";

import PhoneInput from 'react-phone-number-input'
import 'react-phone-number-input/style.css'

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
    children,
    className,
  }: React.ComponentProps<'div'> & {
    theme?: Theme;
  },
) => {
  const classNames = useClassNames(() => {
    const base = `border rounded-md overflow-hidden ${themes.primary['bg-flipped']}`;

    const themeClass = `
      ${themes[theme]['border']}
      ${
        themes[theme === 'primary' ? 'secondary' : theme][
          'focus-within:border-active'
        ]
      }`;

    return [base, themeClass, className];
  }, [theme, className]);

  return <div className={classNames}>{children}</div>
}

const CustomButton = ({ className, ...props }: React.ComponentProps<'button'>) => {
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
  `;

  const classNames = useClassNames(() => {
    return [buttonStyle, className];
  }, [buttonStyle, className])

  return <button {...props} className={classNames} />;
}

const TwitterLogin = ({ text, icon = false }: { text: string, icon?: boolean }) => {
  const supabaseClient = useSupabaseClient();
  return (
    <CustomButton
      className="flex px-4 py-2 items-center justify-center"
      onClick={() => {
        supabaseClient.auth.signInWithOAuth({
          provider: 'twitter',
          options: process.env.NODE_ENV === "development" ? { redirectTo: 'http://localhost:3000' } : {}
        });
      }}
    >
      {icon && <div className="text-cyan-500 pr-2"><FaTwitter /></div>}
      <span>{text}</span>
    </CustomButton>
  )
};


const Header = ({ isLoggedIn }: { isLoggedIn: boolean }) => {
  const supabaseClient = useSupabaseClient();
  // supabaseClient.auth.getSession().then((response) => console.log(response))
  // supabaseClient.auth.updateUser({data: {"phone": 'hiyahiyahiya'}}).then((response) => console.log(response))
  const router = useRouter();
  supabaseClient.auth.getSession().then((res) => console.log(res))
  const titleColor = isLoggedIn ? 'text-white-500' : 'text-gray-700';

  return (
    <div className="max-w-7xl mx-auto py-4 px-4">
      <nav className="relative flex items-center justify-between" aria-label="Global">
          <div className="flex items-center flex-1">
            <div className={`text-2xl font-semibold tracking-tight ${titleColor} cursor-default`}>Transmute</div>
          </div>
          <div className="flex flex-row items-center">
            {!isLoggedIn ? <TwitterLogin text="Login" /> : (
              <CustomButton
                className="px-4 py-2"
                onClick={async () => {
                  await supabaseClient.auth.signOut();
                  router.push('/');
                }}
              >
                Logout
              </CustomButton>
            )}
          </div>
        </nav>
    </div>
  )
}

const LoginPage: NextPage = () => {
  const { isLoading, session, error } = useSessionContext();
  const user = useUser();
  const supabaseClient = useSupabaseClient();
  const [value, setValue] = useState("");
  const [style, setStyle] = useState("");

  useEffect(() => {
    const timeout = setInterval(() => {
      supabaseClient.auth.refreshSession()
    }, 5 * 60 * 1000);
    return () => {
      clearInterval(timeout);
    }
  }, [user, supabaseClient]);

  if (!session) {
    return (
      <div className="w-screen h-screen">
        <Header isLoggedIn={Boolean(session)} />
        {isLoading ? (
          <div className="h-60 flex items-center justify-center">
            <Oval
              height={30}
              width={30}
              color="#06B6D4"
              wrapperStyle={{}}
              wrapperClass=""
              visible={true}
              ariaLabel='oval-loading'
              secondaryColor="#0e7490"
              strokeWidth={4}
              strokeWidthSecondary={4}
            />
          </div>
        ) : (
          <>
          <div className="mt-8 pt-20 mx-auto max-w-7xl px-4">
            <div className="text-center pb-8">
              <h1 className="max-w-4xl mx-auto text-4xl tracking-wide leading-8 font-normal text-gray-700">
                An Endless AI Generated News Feed for You.
              </h1>
              <div className="mt-3 max-w-md font-normal tracking-wide mx-auto text-base text-gray-500">
                <a href="https://www.reddit.com/r/AskReddit/comments/348vlx/what_bot_accounts_on_reddit_should_people_know/">Every account on GPTwitter <i>really is a bot</i>, except you</a>.
              </div>
            </div>
            <div className="my-4 max-w-md mx-auto flex flex-col items-center">
              <TwitterLogin icon text="Login To Enter Your Bubble" />
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
          </>
        )}
      </div>
    );
  }

  const updateUserInfo = () => {
    supabaseClient.auth.updateUser({data: {"phone": value, "style": style}}).then((res) => console.log(res))
  }

  return (
    <div className="min-w-screen w-full min-h-screen h-full bg-[#15202b] text-white">
      <Header isLoggedIn={Boolean(session)} />

      <Center>
        <Stack>
          <Title>Enter a little information below to get started.</Title>
          <TextInput
            label={<Text color="white">Phone Number</Text>}
            placeholder="+10000000000"
            value={value}
            onChange={(event) => setValue(event.currentTarget.value)}
          />
          <Space h="md"/>
          <Select
            label={<Text color="white">Preferred style</Text>}
            placeholder="Pick one"
            data={[
              { value: "classic", label: "Classic Twitter" },
              { value: "informative", label: "Informative" },
              { value: "questions", label: "Thought-provoking Questions" },
            ]}
          />
          <Space h="md"/>
          <Button variant="white" compact color="gray" size="xl" onClick={updateUserInfo}>Enter Feed</Button>
        </Stack>
      </Center>
  </div>
  );
};

export default LoginPage;
