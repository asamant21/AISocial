import React, { useState, useCallback } from "react";
import TweetItem from "./Tweet";
import { Tweet } from "@/lib/types";
import { useRequestCallback } from "@/lib/api";
import { Oval } from "react-loader-spinner";
interface Props {
  tweets?: Tweet[];
}

const Feed = ({ tweets: tweetList }: Props) => {
  const [tweets, setTweets] = useState(tweetList ?? []);
  const [isLoading, setIsLoading] = useState(false);
  const generateTweet = useRequestCallback('/generate');

  const handleGenerate = useCallback(() => {
    setIsLoading(true);
    generateTweet().then(res => {
      const { author, content, id } = res as { author: string, content: string, id: number };
      const tweet =  {
        author: { handle: author },
        content,
        id,
        likes: 0,
        likedByUser: false,
      };
      setIsLoading(false);
      setTweets((curr) => [tweet, ...curr]);
    })
  }, [generateTweet]);

  return (
    <div className="w-70 flex flex-col justify-center items-center">
      <div className="flex flex-row h-10 items-center justify-center">
        {isLoading ? (
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
        ) : (
          <button className="rounded-full bg-cyan-500 py-2 px-4 hover:bg-cyan-700 my-4" onClick={handleGenerate}>Generate</button>
        )}
      </div>

      {tweets.map(tweet => <TweetItem key={tweet.id} tweet={tweet} />)}
    </div>
  );
}

export default Feed;
