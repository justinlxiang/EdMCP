from edapi import EdAPI
import json

def test_api():
    print("Testing Ed API functionality...")
    
    # Initialize and login
    ed = EdAPI()
    login_result = ed.login()
    
    print(f"API Token found: {bool(ed.api_token)}")
    
    if not ed.api_token:
        print("Error: No API token available. Please set up your .env file with ED_API_TOKEN")
        return
    
    # Test get_user_info
    try:
        print("\nTesting get_user_info()...")
        user_info = ed.get_user_info()
        if user_info:
            print(f"Success! User: {user_info['user']['name']}")
            print(f"Email: {user_info['user']['email']}")
            print(f"Role: {user_info['user']['role']}")
            
            # Print available courses
            print("\nAvailable courses:")
            for course in user_info["courses"][:5]:
                print(f"- {course['course']['code']}: {course['course']['name']} (ID: {course['course']['id']})")
        else:
            print("Error: Could not retrieve user info")
    except Exception as e:
        print(f"Error in get_user_info: {str(e)}")
    
    # Only proceed to more tests if we got user info
    if not user_info:
        return
    
    # Get a course ID for testing
    try:
        course_id = user_info["courses"][0]["course"]["id"]
        print(f"\nUsing course ID {course_id} for testing")
        
        # Test list_threads
        print("\nTesting list_threads()...")
        threads = ed.list_threads(course_id, limit=5)
        if threads:
            print(f"Success! Retrieved {len(threads)} threads")
            if threads:
                print("First thread:")
                print(f"- Title: {threads[0]['title']}")
                print(f"- ID: {threads[0]['id']}")
                
                # Save thread ID for further testing
                thread_id = threads[0]['id']
                
                # Test get_thread
                print("\nTesting get_thread()...")
                thread = ed.get_thread(thread_id)
                if thread:
                    print(f"Success! Retrieved thread details for: {thread['thread']['title']}")
                else:
                    print("Error: Could not retrieve thread details")
        else:
            print("Error: Could not retrieve threads")
            
        # Test fetch_posts by keyword
        print("\nTesting fetch_posts by keyword...")
        keyword = "question"  # Example keyword to search for
        print(f"Searching for posts containing: '{keyword}'")
        matching_threads = ed.list_threads(course_id, limit=10)
        matching_threads = [t for t in matching_threads if keyword.lower() in t['title'].lower()]
        if matching_threads:
            print(f"Success! Found {len(matching_threads)} posts containing '{keyword}'")
            for i, thread in enumerate(matching_threads[:3]):  # Show first 3 matches
                print(f"{i+1}. {thread['title']} (ID: {thread['id']})")
        else:
            print(f"No posts found containing '{keyword}'")
            
    except Exception as e:
        print(f"Error in thread tests: {str(e)}")
        
    print("\nTesting complete")

if __name__ == "__main__":
    test_api() 