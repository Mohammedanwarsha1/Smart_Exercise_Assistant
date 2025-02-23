<script setup>
// Your Vue script logic (if any)
</script>

<template>
  <div class="site-container">
    <!-- Navbar -->
    <nav>
      <RouterLink :to="{ name: 'Home' }" class="nav__header">
        
        <span class="big-text">Fitness Corrector</span>

      </RouterLink>
    </nav>

    <!-- Main Content -->
    <main>
      <Transition name="fade" mode="out-in">
      <!-- Page View -->
        <RouterView />
      </Transition>
    </main>
  </div>
</template>

<style lang="scss">

/* Global body styles */
body {
  font-family: Georgia, 'Times New Roman', Times, serif; 
}

/* Site Container */
.site-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navbar Styles */
nav {
  margin: 3rem 0;
  text-align: center;

  .nav__header {
    font-size: 2rem;
    margin-top: 10%;
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-weight: 700;
    text-shadow: D#dadcee;
    
    letter-spacing: 1px;
    color: #0015ff;
  }

  /* Small "Welcome to" text 
  .small-text {
    font-size: 1.2rem;
    font-style: italic;
    font-weight: normal;
    opacity: 0;
    transform: translateY(10px);
    animation: fadeIn 1s ease-out forwards;

   
}*/
  

  /* Large "Fitness Corrector" text */
  .big-text {
    font-size: 2.5rem;
    font-weight: bold;
    font-style: italic;
    opacity: 0;
    transform: translateY(20px);
    animation: fadeIn 1s ease-out 0.5s forwards; /* Delayed animation */
    display: block;
  }

}
/* Fade-in & Slide-up Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Page Transition Animations */
/* Page Transition Animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.6s ease-in-out;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}


/* Main content styling */
main {
  margin-inline: auto;
  width: 90vw;
}
</style>
