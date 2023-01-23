import React, { useState, useCallback, useEffect } from "react";
import { Tweet } from "@/lib/types";

interface Props {
  tweet: Tweet
}

const Tweet = ({ tweet }: Props) => {
  const { id, author, content, likes, likedByUser } = tweet;
  const [liked, setLiked] = useState(likedByUser);

  const handleToggleLike = useCallback(() => {
    // Optimistic update before we receive ground truth from backend.
    setLiked((curr) => !curr);

    // Update the backend.
    fetch(`/api/tweets/${id}/like`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    })

  }, [id]);

  useEffect(() => {
    setLiked(likedByUser);
  }, [likedByUser]);

  const color = liked ? "red" : "gray";

  return (
    <div className='p-4 cursor-pointer border-b border-zinc-700 hover:bg-gray-600 hover:bg-opacity-30'>
      <div className='flex items-start justify-stretch space-x-3'>
        {/*
        <img
          src={author.img}
          alt=''
          className='rounded-full w-7 h-7 sm:h-10 sm:w-10'
        />
          */}
        <div className='flex flex-col  space-y-2 text-sm flex-1'>
          <div className='flex space-x-2 items-center'>
            <span className='font-bold'>&middot;</span>
            <p className='text-xs sm:text-sm font-light hover:underline'>
              @{author.handle}
            </p>
          </div>
          <p className='text-sm text-justify whitespace-pre-line'>
            {content}
          </p>

          <div className='flex items-center justify-between mt-1'>
            <div className={`text-${color}-700 text-sm  flex items-center space-x-2 bg-transparent  hover:bg-slate-100 rounded-3xl hover:bg-opacity-10 p-2 hover:text-sky-400`}>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
              <p className='text-white'>{likes}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Tweet;
