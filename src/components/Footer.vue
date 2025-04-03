<template>
        <div class="fixed bottom-0 w-[360px] flex justify-between px-1 py-3 cursor-pointer border-t border-gray-300 italic bg-white ">
            <div class="flex-1 flex flex-col items-center text-blue-500 relative gap-3 ">
                <div class="relative">
                    <img src="/src/assets/icons/home.svg" alt="">
                    <span class="absolute -top-2 -right-3 bg-blue-500 text-white text-xs font-bold w-5 h-5 flex items-center justify-center rounded-full">5</span>
                </div>
                <p class="text-xs italic"> 
                            <RouterLink to="/main">Продаю</RouterLink>
                </p>
            </div>

            <div class=" gap-3 flex-1 flex flex-col items-center text-gray-400 hover:text-blue-500 transition">
                <img src="/src/assets/icons/shape.svg" alt="">
                <p class="text-xs italic">
                    <RouterLink to="/buyitems">Куплю</RouterLink>
                </p>
                
            </div>

        
                    <div class="gap-2 flex-1 flex flex-col items-center text-gray-400 hover:text-blue-500 transition">
                    <img src="/src/assets/icons/ic_plusgray.svg" alt="">
                        <p class="text-xs italic"> 
                            <RouterLink to="/create">Создать</RouterLink>
                        </p>
                </div>
        

            <div class="gap-2 flex-1 flex flex-col items-center text-gray-400 hover:text-blue-500 transition">
                <img src="/src/assets/icons/message-circle-lines.svg" alt="">
                    <p class="text-xs italic"> 
                        <RouterLink to="/message">Сообщения</RouterLink>
                    </p>           
            </div>

            <div class=" gap-3 flex-1 flex flex-col items-center text-gray-400 hover:text-blue-500 transition">
                <img src="/src/assets/icons/profile.png" alt="">
                <p class="text-xs italic"><RouterLink to="/profile">Профиль</RouterLink></p>
            </div>
            </div>
</template>



