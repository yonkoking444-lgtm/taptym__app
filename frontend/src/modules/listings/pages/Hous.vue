<script setup>  
import Header from '../../../components/Header.vue';
import Footer from '../../../components/Footer.vue';
import EmptyRequests from '../../../components/EmptyRequests.vue';
</script>

<template>
    <div class="container max-w-sm flex flex-col h-screen gap-4  italic">  
        <header>
            <Header/>
        </header>
        <main class="flex flex-col overflow-y-auto flex-grow min-h-0 my-20 gap-4 mt-27">
            <EmptyRequests/>
        </main>
        <footer>
            <Footer/>
        </footer>
        </div>
    </template>