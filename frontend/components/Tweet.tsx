import React, { useState, useCallback, useEffect } from "react";
import { TwitterShareButton } from "react-share";
import { TwitterIcon } from "react-share";
import { Tweet } from "@/lib/types";
import { useRequestCallback } from "@/lib/api";

interface Props {
  tweet: Tweet
}

const Tweet = ({ tweet }: Props) => {
  const { id, author, content, likes, likedByUser } = tweet;
  const [liked, setLiked] = useState(likedByUser);
  const likeTweet = useRequestCallback(`/like/${id}`);

  const handleToggleLike = useCallback(() => {
    // Optimistic update before we receive ground truth from backend.
    setLiked((curr) => !curr);
    console.log("toggle like");
    if (!liked) {
      likeTweet();
    }
  }, [liked, likeTweet]);

  useEffect(() => {
    setLiked(tweet.likedByUser);
  }, [tweet]);

  const color = liked ? "#F91880" : "#71767B";

  return (
    <div className='p-4 cursor-pointer border-b border-zinc-700 hover:bg-gray-600 hover:bg-opacity-30 w-1/2 align-items: center'>
      <div className='flex flex-row items-start justify-between space-x-3'>
        <div className='flex flex-col space-y-2 text-sm flex-3 items-start justify-stretch'>
          <div className='flex flex-col flex-1'>
            <div className='flex space-x-2 items-center pb-2'>
              <p className='text-xs sm:text-sm font-light hover:underline'>
                <b>{author.handle}</b>
              </p>
            </div>
            <p className='text-sm whitespace-pre-line'>
              {content}
            </p>
          </div>
        </div>
        <div className='flex flex-row flex-1 flex-2'>
          <div className='flex items-center justify-between mt-1' onClick={handleToggleLike}>
            <div className={`text-[${color}] text-sm  flex items-center space-x-2 bg-transparent  hover:bg-slate-100 rounded-3xl hover:bg-opacity-10 p-2 hover:text-sky-400`}>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" strokeWidth={1.5} stroke={color} fill={liked ? color : "none"} className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
            </div>
          </div>
          <div className='flex items-center justify-between mt-1'>
          <TwitterShareButton url={"https://gptwitter-neon.vercel.app/"} title={content + "\n-" + author.handle + "\n\nThis tweet was generated with GPTwitter."}> 
            <TwitterIcon round size={30} />
          </TwitterShareButton>
        </div>
        </div>
      </div>
    </div>
  );
}

export default Tweet;