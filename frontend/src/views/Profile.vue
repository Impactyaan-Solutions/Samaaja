  <script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import { useI18n } from 'vue-i18n'
  import {
    ChevronDown,
    Leaf,
    Droplets,
    BookOpen,
    Settings,
    LogOut // Added for the menu
  } from 'lucide-vue-next'
  import { Heart, MessageSquare } from 'lucide-vue-next'
  import AppHeader from '@/components/common/AppHeader.vue'
  import { authState } from '@/auth'
  import { getProfile } from '@/services/api'
  import { getUserProfilePosts, getUserProfileActions } from '@/services/api'
  import PostActionDialouge from '../components/common/PostActionDialouge.vue'

  const { t } = useI18n()
  // --- Menu Logic ---
  const isMenuOpen = ref(false)
  const userPosts = ref([])
  const userActions = ref([])
  const postsLoading = ref(false)
  const actionsLoading = ref(false)
  const activeTab = ref('actions')
  const postsError = ref("")
  const actionsError = ref("")
  const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
  }

  const handleLogout = () => {
    // Replace with your actual logout logic (e.g., authState.logout())
 //   console.log("Logging out...")
    isMenuOpen.value = false
  }

  const goToSettings = () => {
    // Replace with your navigation logic (e.g., router.push('/settings'))
   // console.log("Navigating to settings...")
    isMenuOpen.value = false
  }

  // --- Original User Logic ---
  const route = useRoute()
  const externalProfile = ref(null)
  const isExternalLoading = ref(false)

  const loadExternalProfile = async (email) => {
    
    isExternalLoading.value = true
    try {
      const data = await getProfile(email)
      externalProfile.value = data
      
    } catch (err) {
      
      externalProfile.value = null
    } finally {
      isExternalLoading.value = false
    }
  }

  onMounted(() => {
    fetchActions()
   
    if (route.query.user_email) {
      loadExternalProfile(route.query.user_email)
    }
      
  })
  watch(
    () => authState.isInitialLoad,
    (val) => {
  //    console.log("authState.isInitialLoad =")
    },
    { immediate: true }
  )
  watch(() => route.query.user_email, (newEmail) => {
    if (newEmail) {
      loadExternalProfile(newEmail)
    
    } else {
      externalProfile.value = null
    }
    
  })

  const user = computed(() => {
    if (externalProfile.value) {
      const p = externalProfile.value
      return {
        name: p.full_name,
        role: p.user_category,
        bio: p.bio,
        image: p.user_image,
        stats: {
          actions: p.action_count || 0,
          issuesResolved: p.issues_reported || 0,
          posts: p.posts || 0,
          hours: p.hours_invested || 0
        },
        interests: p.interests,
        badges: p.badges
      }
    }

    return {
      name: authState.profile.fullName,
      role: authState.profile.category,
      bio: authState.profile.bio, 
      image: authState.profile.imageBase64 || authState.profile.image,
      stats: {
        actions: authState.profile.stats.actions,
        issuesResolved: authState.profile.stats.issuesReported || 0,
        posts: authState.profile.stats.posts || 0,
        hours: authState.profile.stats.hours || 0
      },
      interests: authState.profile.interests,
      badges: authState.profile.badges
    }
  })

  const isLoading = computed(() => authState.isInitialLoad || isExternalLoading.value)
  const fetchPosts = async () => {
    postsLoading.value = true
    postsError.value = ""

    try {
    const email = route.query.user_email || authCache.email
      const data = await getUserProfilePosts(email)

      userPosts.value = data.posts || []
      
    } catch (err) {
     // console.error(err)
      postsError.value = t('profile.failedToLoadPosts')
    } finally {
      postsLoading.value = false
    }
  }
  const authCache = JSON.parse(
    localStorage.getItem("samaaja_auth_cache") || "{}"
  );
  /// fetch actions 
  const fetchActions = async () => {
    //console.log("Fetching actions for user:", route.query.user_email || authCache.email)
    actionsLoading.value = true
    actionsError.value = ""

    try {
    const email = route.query.user_email ||authCache.email
  //  console.log("user email",email)
      const data = await getUserProfileActions(email)
      userActions.value = data.actions || []
     // console.log("Fetched actions:", userActions.value)
    } catch (err) {
     // console.error(err)
      actionsError.value = t('profile.failedToLoadActions')
    } finally {
      actionsLoading.value = false
    }
  }
  // watch(
  //   () => route.query.user_email,
  //   async (newEmail) => {
  //     if (newEmail) {
  //       await loadExternalProfile(newEmail)
  //     } else {
  //       externalProfile.value = null
  //     }

    
  //   }
  // )

watch(activeTab,async(newTab)=>{
  if(newTab === 'actions' && userActions.value.length === 0) {
   
    await fetchActions()
  } else if(newTab === 'posts' && userPosts.value.length === 0) {
   
    await fetchPosts()
  }
})
// Helper: single source of truth for "whose profile are we viewing"
const viewedEmail = computed(() => route.query.user_email || authCache.email)

watch(
  () => route.query.user_email,
  async (newEmail) => {
    if (newEmail) {
      await loadExternalProfile(newEmail)
    } else {
      externalProfile.value = null
    }

    // Clear stale data immediately so old user's posts/actions don't flash
    userActions.value = []
    userPosts.value = []
    actionsError.value = ""
    postsError.value = ""

    // Refetch whichever tab is currently active
    if (activeTab.value === 'actions') {
      await fetchActions()
    } else {
      await fetchPosts()
    }
  },
  { immediate: false } // onMounted already handles the initial load
)
  const truncate = (text, length = 50) => {
  
    return text.length > length ? text.slice(0, length) + "..." : text;
  };

  const selectedItem = ref(null)
  const isDialogOpen = ref(false)

  const isMobile = () => {
    return window.innerWidth < 768
  }

  const openDialog = (item) => {
    selectedItem.value = item
    isDialogOpen.value = true
  }

  const closeDialog = () => {
    isDialogOpen.value = false
    selectedItem.value = null
  }


  </script>

  <template>
    <div v-if="!isLoading" class="min-h-full bg-gray-50/50 pb-6 relative">
      
      <!-- Header: Now listening for the @menuClick event -->
      <AppHeader @menuClick="toggleMenu" />

      <!-- Dropdown Menu -->
      <transition
        enter-active-class="transition duration-100 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-75 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
        <div 
          v-if="isMenuOpen" 
          class="absolute right-5 top-16 w-48 bg-white rounded-2xl shadow-xl border border-gray-100 z-50 overflow-hidden"
        >
          <div class="flex flex-col py-1">
            <!-- Settings Tab -->
            <button 
              @click="goToSettings" 
              class="flex items-center space-x-3 px-4 py-3 hover:bg-gray-50 text-gray-700 transition-colors"
            >
              <Settings class="w-4 h-4 text-gray-500" />
              <span class="text-sm font-medium">{{ t('menu.settings') }}</span>
            </button>

            <div class="border-t border-gray-100 mx-2"></div>

            <!-- Logout Tab -->
            <button
              @click="handleLogout"
              class="flex items-center space-x-3 px-4 py-3 hover:bg-red-50 text-red-600 transition-colors"
            >
              <LogOut class="w-4 h-4" />
              <span class="text-sm font-medium">{{ t('menu.logout') }}</span>
            </button>
          </div>
        </div>
      </transition>

      <!-- Invisible Backdrop: Closes menu when clicking anywhere else -->
      <div 
        v-if="isMenuOpen" 
        @click="isMenuOpen = false" 
        class="fixed inset-0 z-40"
      ></div>

      <!-- Original Profile Content -->
      <div class="px-5 pb-2 rounded-2xl shadow-sm mb-5">
        <div class="flex flex-col items-center p-2 px-4 text-center">
          <!-- Avatar -->
          <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 border-4 border-white shadow-lg mb-4">

            <!-- User Image -->
            <img 
              v-if="user.image"
              :src="user.image" 
              class="w-full h-full object-cover"
              @error="user.image = null"
            />

            <!-- Fallback SVG -->
            <svg
            v-else
            viewBox="0 0 120 120"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <!-- Background -->
            <circle cx="60" cy="60" r="60" fill="#EEF2FF"/>

            <!-- Decorative Circle -->
            <circle cx="60" cy="60" r="52" fill="#E0E7FF"/>

            <!-- Head -->
            <circle cx="60" cy="42" r="20" fill="#6366F1"/>

            <!-- Body -->
            <path
              d="M30 98C30 80.3269 43.3269 67 61 67C78.6731 67 92 80.3269 92 98V120H30V98Z"
              fill="#6366F1"
            />

            <!-- Shine -->
            <circle cx="52" cy="36" r="4" fill="#A5B4FC" fill-opacity="0.7"/>
          </svg>

          </div>
          
          <h1 class="text-2xl font-bold text-gray-900">{{ user.name }}</h1>
          <p class="text-blue-600 font-semibold text-sm mt-1">{{ user.role }}</p>
          
          <p 
            v-if="user.bio" 
            class="text-gray-500 italic text-sm mt-4 px-2 tracking-wide leading-relaxed"
          >
            {{ user.bio }}
          </p>

          <!-- Tags -->
          <div class="flex items-center space-x-3 mt-6">
            <!-- Render interests -->
            <div 
              v-for="(interest, index) in user.interests"
              :key="index"
              class="bg-blue-50/80 px-4 py-2 rounded-2xl flex flex-col items-center shadow-sm border border-blue-100/50"
            >
              <img :src="interest.icon" class="w-8 h-8 mb-1 rounded-full"/>
              <span class="text-[11px] font-bold text-gray-700">{{ interest.action_category?.trim() }}</span>
            </div>
          </div>

        </div>
      </div>

      <!-- Impact Summary -->
      <div class="px-5 mb-5">
        <div class="flex items-center space-x-2 mb-4">
          <span class="text-xl">🌟</span>
          <h3 class="font-bold text-gray-900 text-lg">{{ t('profile.impactSummary') }}</h3>
        </div>

        <div class="grid grid-cols-3 gap-3">
          <div class="bg-white border border-gray-100 rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
            <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.actions }}</span>
            <span class="text-[11px] text-gray-500 font-medium leading-tight">{{ t('profile.actions') }}</span>
          </div>
          <div class="bg-white border border-gray-100  rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
            <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.hours }}</span>
            <span class="text-[11px] text-gray-500 font-medium leading-tight">{{ t('profile.hours') }}</span>
          </div>
          <div class="bg-white border border-gray-100  rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
            <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.posts }}</span>
            <span class="text-[11px] text-gray-500 font-medium leading-tight">{{ t('profile.posts') }}</span>
          </div>
        </div>
      </div>

      <!-- Badges -->
      <div class="px-5 mb-20">
        <div class="flex items-center space-x-2 mb-4">
          <span class="text-xl">🥇</span>
          <h3 class="font-bold text-gray-900 text-lg">{{ t('profile.badgesEarned') }}</h3>
        </div>
        <div v-if="user.badges" class="grid grid-cols-3 gap-3">
          <div v-for="(badge, index) in user.badges" :key="index" class="flex flex-col justify-center items-center text-center">
            <img :src="badge.badge_icon" class="w-8 h-8 mb-1 rounded-full"/>
            <span class="text-[11px] text-gray-500 font-medium leading-tight">{{ badge.badge_name }}</span>
          </div>
        </div>
        <div v-else class="bg-white border border-gray-100 p-6 rounded-2xl shadow-sm italic text-gray-400 text-sm text-center">
          {{ t('profile.noBadges') }}
        </div>
      </div>
        <div class="px-5 mb-4">
    <div class="flex bg-blue-100 rounded-lg p-1">
      <button 
        @click="
    activeTab = 'actions';
  "
        :class="[
          'flex-1 py-2 text-sm font-medium rounded-md transition-all',
          activeTab === 'actions'
            ? 'bg-white text-gray-900 shadow'
            : 'text-gray-600'
        ]"
      >
        {{ t('profile.actionsTab') }}
      </button>

      <button
        @click="
    //console.log('Posts clicked');
    activeTab = 'posts';
  "
        :class="[
          'flex-1 py-2 text-sm font-medium rounded-md transition-all',
          activeTab === 'posts'
            ? 'bg-white text-gray-900 shadow'
            : 'text-gray-600'
        ]"
      >
        {{ t('profile.postsTab') }}
      </button>
    </div>
   
  <div class="mt-4 space-y-4">
  <!-- Actions tab -->
  <div v-if="activeTab === 'actions'">
    <div v-if="actionsLoading" class="text-center py-6">{{ t('profile.loadingActions') }}</div>
    <div v-else-if="actionsError" class="text-center text-red-500 py-6">{{ actionsError }}</div>
    <div v-else-if="userActions.length === 0" class="text-center text-gray-500 py-6">{{ t('profile.noActionsFound') }}</div>
    <div v-else>
      <div
        v-for="action in userActions"
        :key="action.id"
        class="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm"
        @mouseenter="!isMobile() && openDialog(action)"
        @click="isMobile() && openDialog(action)"
      >
        <p class="text-[10px] uppercase font-semibold text-gray-400 mb-1">{{ t('profile.actionLabel') }}</p>
        <h3 class="font-bold text-gray-900">{{ action.title }}</h3>
        <p class="text-sm text-gray-500 mt-2">{{ truncate(action.description) }}</p>
        <div class="flex items-center gap-2 text-xs mt-3">
          <span class="text-green-600 font-medium">{{ action.status }}</span>
        </div>
      </div>
    </div>
  </div>

    <!-- Posts -->
   <div v-else>
    <div v-if="postsLoading" class="text-center py-6">{{ t('profile.loadingPosts') }}</div>
    <div v-else-if="postsError" class="text-center text-red-500 py-6">{{ postsError }}</div>
    <div v-else-if="userPosts.length === 0" class="text-center text-gray-500 py-6">{{ t('profile.noPostsFound') }}</div>
    <div v-else>
      <div
        v-for="post in userPosts"
        :key="post.id"
        class="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm"
        @mouseenter="!isMobile() && openDialog(post)"
        @click="isMobile() && openDialog(post)"
      >
        <p class="text-[10px] uppercase font-semibold text-gray-400 mb-1">{{ t('profile.postLabel') }}</p>
        <h3 class="font-bold text-gray-900">{{ post.title }}</h3>
        <p class="text-sm text-gray-500 mt-2">{{ truncate(post.description) }}</p>
        <div class="px-4 py-3 border-t border-gray-50 flex items-center justify-between">
          <div class="flex items-center space-x-6">
            <button class="flex items-center space-x-1.5 text-gray-500 hover:text-red-500 transition-colors">
              <Heart class="w-5 h-5" />
              <span class="text-xs font-semibold">{{ post.like_count }}</span>
            </button>
            <button class="flex items-center space-x-1.5 text-gray-500 hover:text-primary-500 transition-colors">
              <MessageSquare class="w-5 h-5" />
              <span class="text-xs font-semibold">{{ post.comment_count }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</div>
      <PostActionDialouge
    :show="isDialogOpen"
    :item="selectedItem"
    @close="closeDialog"
  />
    </div>



    <!-- Loading State -->
    <div v-else class="h-screen flex items-center justify-center bg-white">
      <div class="flex flex-col items-center space-y-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="text-gray-500 font-medium tracking-wide">{{ t('profile.loading') }}</p>
      </div>
    </div>
  </template>