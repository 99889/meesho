// User Tracking Utility
// Generates and maintains a unique user ID for each visitor

const USER_ID_KEY = 'meesho_user_id';
const USER_DATA_KEY = 'meesho_user_data';

/**
 * Generate a unique user ID
 */
const generateUserId = () => {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 15);
  return `user_${timestamp}_${random}`;
};

/**
 * Get or create user ID
 */
export const getUserId = () => {
  let userId = localStorage.getItem(USER_ID_KEY);
  
  if (!userId) {
    userId = generateUserId();
    localStorage.setItem(USER_ID_KEY, userId);
    
    // Initialize user data
    const userData = {
      userId,
      createdAt: new Date().toISOString(),
      visits: 1,
      lastVisit: new Date().toISOString(),
    };
    localStorage.setItem(USER_DATA_KEY, JSON.stringify(userData));
  } else {
    // Update visit count
    updateUserVisit();
  }
  
  return userId;
};

/**
 * Update user visit data
 */
const updateUserVisit = () => {
  const userDataStr = localStorage.getItem(USER_DATA_KEY);
  if (userDataStr) {
    const userData = JSON.parse(userDataStr);
    userData.visits = (userData.visits || 0) + 1;
    userData.lastVisit = new Date().toISOString();
    localStorage.setItem(USER_DATA_KEY, JSON.stringify(userData));
  }
};

/**
 * Get user data
 */
export const getUserData = () => {
  const userDataStr = localStorage.getItem(USER_DATA_KEY);
  return userDataStr ? JSON.parse(userDataStr) : null;
};

/**
 * Track user event
 */
export const trackEvent = (eventName, eventData = {}) => {
  const userId = getUserId();
  const event = {
    userId,
    eventName,
    eventData,
    timestamp: new Date().toISOString(),
  };
  
  // Store in localStorage (you can send to backend later)
  const eventsKey = 'meesho_user_events';
  const eventsStr = localStorage.getItem(eventsKey);
  const events = eventsStr ? JSON.parse(eventsStr) : [];
  events.push(event);
  
  // Keep only last 100 events
  if (events.length > 100) {
    events.shift();
  }
  
  localStorage.setItem(eventsKey, JSON.stringify(events));
  
  console.log('Event tracked:', event);
  return event;
};

/**
 * Get user events
 */
export const getUserEvents = () => {
  const eventsStr = localStorage.getItem('meesho_user_events');
  return eventsStr ? JSON.parse(eventsStr) : [];
};

// Initialize user ID on module load
getUserId();
