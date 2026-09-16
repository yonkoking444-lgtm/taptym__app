    <template>
        <div class="flex items-center justify-between p-4 border-b border-stone-300 cursor-pointer hover:bg-gray-100">
        <div class="flex items-center">
            <span class="text-blue-500 text-xl font-base">
                <img :src="heshteg" alt="icon">

            </span>
            <span class="ml-3 text-lg font-base text-black">{{ text }}</span>
        </div>
        <span class="text-gray-400 text-xl">
            <img src="/src/assets/icons/ic_chevron_right.svg" alt="chevron">
        </span>
        </div>
    </template>
    
    <script setup>
    
    defineProps({
        text: {
            type: String,
            required: true, 
        },
        heshteg:{
            type: String,
            required: true, 
        }
    });

    </script>
    