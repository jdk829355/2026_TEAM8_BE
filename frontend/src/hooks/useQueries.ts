import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

// User Profile
export const useUserProfile = () => {
  return useQuery({
    queryKey: ['userProfile'],
    queryFn: async () => {
      const { data } = await api.get('/user/profile');
      return data;
    },
    staleTime: 5 * 60 * 1000,
  });
};

// My Matchings
export const useMyMatchings = () => {
  return useQuery({
    queryKey: ['myMatchings'],
    queryFn: async () => {
      const { data } = await api.get('/matching/my');
      return data;
    },
    staleTime: 5 * 60 * 1000,
  });
};

// My Tasks (TODOs)
export const useMyTasks = () => {
  return useQuery({
    queryKey: ['myTasks'],
    queryFn: async () => {
      const { data } = await api.get('/todo/my-tasks');
      return data;
    },
    staleTime: 1 * 60 * 1000,
  });
};

export const useOpponentTasks = (matchingId: string | null) => {
  return useQuery({
    queryKey: ['opponentTasks', matchingId],
    queryFn: async () => {
      if (!matchingId) return null;
      const { data } = await api.get(`/todo/${matchingId}/opponent-tasks`);
      return data;
    },
    enabled: !!matchingId,
    staleTime: 1 * 60 * 1000,
  });
};

// Announcements
export const useAnnouncements = () => {
  return useQuery({
    queryKey: ['announcements'],
    queryFn: async () => {
      const { data } = await api.get('/announcement/all');
      return data;
    },
    staleTime: 5 * 60 * 1000,
  });
};

// Chat Rooms
export const useChatRooms = () => {
  return useQuery({
    queryKey: ['chatRooms'],
    queryFn: async () => {
      const { data } = await api.get('/chat/rooms');
      return data;
    },
    staleTime: 1 * 60 * 1000,
    // Polling could be enabled here if we want pseudo real-time, but websockets are better
    // refetchInterval: 5000, 
  });
};

// Chat History
export const useChatHistory = (roomId: string | null) => {
  return useQuery({
    queryKey: ['chatHistory', roomId],
    queryFn: async () => {
      if (!roomId) return [];
      const { data } = await api.get(`/chat/room/${roomId}`);
      return data;
    },
    enabled: !!roomId,
    staleTime: 0,
    gcTime: 0,
  });
};
