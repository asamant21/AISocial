import React from "react";
import TweetItem from "./Tweet";
import { Tweet } from "@/lib/types";

interface Props {
  tweets: Tweet[];
}

const Feed = ({ tweets }: Props) => {
  return (
    <div>
      {tweets.map(tweet => <TweetItem key={tweet.id} tweet={tweet} />)}
    </div>
  );
}

export default Feed;
