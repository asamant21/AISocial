type Author = {
  handle: string;
}

export type Tweet = {
  id: number;
  author: Author;
  content: string;
  metadata: Object;
  likes: number;
  likedByUser: boolean;
}
