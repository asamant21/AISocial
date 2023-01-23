import React, { useState, useCallback } from "react";
import TweetItem from "./Tweet";
import { Tweet } from "@/lib/types";
import { useRequestCallback } from "@/lib/api";

interface Props {
  tweets?: Tweet[];
}

const Feed = ({ tweets: tweetList }: Props) => {
  const [tweets, setTweets] = useState(tweetList ?? []);
  const generateTweet = useRequestCallback('/generate');

  const handleGenerate = useCallback(() => {
    generateTweet().then(res => {

      const { author, content, id } = res as { author: string, content: string, id: number };
      const tweet =  {
        author: { handle: author },
        content,
        id,
        likes: 0,
        likedByUser: false,
      };
      setTweets((curr) => [tweet, ...curr]);
    })
  }, [generateTweet]);

  return (
    <div className="w-70 justify-center items-center flex flex-col">
      <button className="rounded-full bg-cyan-500 py-2 px-4 hover:bg-cyan-700 my-4" onClick={handleGenerate}>Generate</button>

      {tweets.map(tweet => <TweetItem key={tweet.id} tweet={tweet} />)}
    </div>
  );
}

export default Feed;
