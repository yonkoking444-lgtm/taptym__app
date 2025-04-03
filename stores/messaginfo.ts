import { defineStore } from "pinia";

export const useChatStore = defineStore("chat", {
    state: () => ({
        title: "Куплю Тайота Камри 25",
        imageUrl: "/src/assets/images/camry.svg",
        iconUrl: "/src/assets/icons/ic_backblack.svg",
        lastMessage: "Здавствуйте! Да цену можем...",
        time: "11:52",
        name: "Темирлан"
    }),
    actions: {
        updateLastMessage(newMessage: string, newTime: number, newTitle: string, newName: string,) {
        this.lastMessage = newMessage;
        this.time = newTime;
        this.name = newName;
        this.title = newTitle;
        },
        changeImage(newImage: string, newIcon: string,) {
        this.imageUrl = newImage;
        this.iconUrl = newIcon
        },
    },
    });

