import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

type ThemeStorage = {
  theme: string;
  setTheme: (theme: string) => void;
};

export const useThemeStorage = create<ThemeStorage>()(
  persist(
    (set) => ({
      theme: "lofi",
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: "theme",
      storage: createJSONStorage(() => localStorage),
    }
  )
);
