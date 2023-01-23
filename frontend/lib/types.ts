type Author = {
  handle: string;
}

export type Tweet = {
  id: number;
  author: Author;
  content: string;
  likes: number;
  likedByUser: boolean;
}
