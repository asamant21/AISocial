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
  const [isReset, setIsReset] = useState(false)
  const generateTweet = useRequestCallback('/generate');
  const regenerateTweet = useRequestCallback('/regenerate');
  const [hover, setHover] = useState(false)

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
    }).catch(() => {
      setIsLoading(false);
    });
  }, [generateTweet]);

  const handleRegenerate = useCallback(() => {
    setIsReset(true);
    regenerateTweet().then(res => {
      const { author, content, id } = res as { author: string, content: string, id: number };
      const tweet =  {
        author: { handle: author },
        content,
        id,
        likes: 0,
        likedByUser: false,
      };
      setIsReset(false);
      setTweets([tweet]);
    }).catch(() => {
      setIsReset(false);
    });
  }, [regenerateTweet]);

  return (
    <div className="flex flex-col justify-center items-center">
      <div className="flex flex-row h-10 items-center justify-center mt-10 my-3">
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
          <button className="rounded-full bg-cyan-500 py-2 px-4 hover:bg-cyan-700 mt-4" onClick={handleGenerate}>Generate</button>
        )}
      </div>
      {tweets.length > 0 ? 
        <div className="flex flex-row h-10 items-center justify-center">
            <button 
              className="px-4" 
              style={{
                color: hover ? "#C1C1C1" : "#808996", 
                fontSize: "15px", 
              }} 
              onMouseEnter={() => setHover(true)} 
              onMouseLeave={() => setHover(false)}
              onClick={handleRegenerate}
            >
              Reset
            </button>
        </div> : <></>
      }
      {isReset? 
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
           />: 
           <div className="w-[32rem] max-w-full">
           {tweets.map(tweet => <TweetItem key={tweet.id} tweet={tweet} />)}
          </div>}
    </div>
  );
}

export default Feed;
