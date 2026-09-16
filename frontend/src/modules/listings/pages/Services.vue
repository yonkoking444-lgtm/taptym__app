<template>
<div class="container flex flex-col justify-center h-screen max-w-sm gap-4 italic">  
    <Header/>
    <EmptyRequests/>
    <Footer/>
    </div>
</template>


    
    <script setup>  
        import Header from '../../../components/Header.vue';
        import Footer from '../../../components/Footer.vue';
        import Othercom from '../../../components/Othercom.vue';
        import EmptyRequests from '../../../components/EmptyRequests.vue';
        
        
    </script>