<template>
<div class="container max-w-sm flex flex-col h-screen gap-4 justify-center italic">  
    <Header/>
    <EmptyRequests/>
    <Footer/>
    </div>
</template>



<script setup>  
import Header from '../../../components/Header.vue';
import Othercom from '../../../components/Othercom.vue';
import EmptyRequests from '../../../components/EmptyRequests.vue';
import Footer from '../../../components/Footer.vue';
</script>