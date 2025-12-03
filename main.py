import streamlit as st
from io import StringIO
import json
import os

st.set_page_config(layout='wide')

files = st.sidebar.file_uploader("Please upload a learning sets", accept_multiple_files=True)

def init(n=True):
    if "step" not in st.session_state or n:
        st.session_state.step = 0

if not os.path.exists('review.json'):
    with open('review.json', 'w') as f:
        json.dump({}, f)

idx = st.sidebar.radio(
    'choose a learning set', 
    range(len(files)),
    format_func=lambda x: files[x].name,
    on_change=init
)

review_mode = st.sidebar.checkbox('Review Mode', on_change=init)
mask_mode = st.sidebar.checkbox('Hide Answer', value=True)

init(False)

if files:
    learnset_raw = StringIO(files[idx].getvalue().decode("utf-8")).read().strip().split('\n')
    learnset = [[learnset_raw[i], learnset_raw[i+1]] for i in range(0,len(learnset_raw), 2)]
    
    current_filename = files[idx].name

    if review_mode:
        with open('review.json', 'r') as f:
            review_data = json.load(f)
        learnset = review_data.get(current_filename, [])
        if not learnset:
            st.error("No review data for this file.")
            st.stop()

    per = (st.session_state.step + 1) / len(learnset)
    st.sidebar.progress(per if per <= 1 else 1, text=f'for completion {st.session_state.step + 1}/{len(learnset)}')

    with open('review.json', 'r') as f:
        cnt_data = json.load(f)
    review_count = len(cnt_data.get(current_filename, []))

    st.sidebar.json(
        {
            'target' : current_filename,
            'mode': 'review' if review_mode else 'normal',
            'review_count': review_count,
            **st.session_state
        }
    )

    col1, col2, col3 = st.columns(3)

    prev = col1.button('prev', use_container_width=True)
    next = col2.button('next', use_container_width=True)
    
    if review_mode:
        action_btn = col3.button('delete from review', use_container_width=True)
    else:
        action_btn = col3.button('add to review', use_container_width=True)

    if prev: 
        if st.session_state.step != 0:
            st.session_state.step -=1
        st.rerun()
        
    if next:
        if st.session_state.step <= len(learnset) - 2:
            st.session_state.step +=1
        st.rerun()

    if action_btn:
        with open('review.json', 'r') as f:
            data = json.load(f)
        
        if current_filename not in data:
            data[current_filename] = []
            
        current_card = learnset[st.session_state.step]

        if review_mode:
            if current_card in data[current_filename]:
                data[current_filename].remove(current_card)
                with open('review.json', 'w') as f:
                    json.dump(data, f)
                if st.session_state.step >= len(data[current_filename]) and st.session_state.step > 0:
                    st.session_state.step -= 1
                st.rerun()
        else:
            if current_card not in data[current_filename]:
                data[current_filename].append(current_card)
                with open('review.json', 'w') as f:
                    json.dump(data, f)
            if st.session_state.step <= len(learnset) - 2:
                st.session_state.step +=1
            st.rerun()

    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')

    k = st.container()

    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')

    v = st.container()

    if learnset:
        k.markdown(f'### {learnset[st.session_state.step][0]}')
        
        if mask_mode:
            with v.expander("Check Answer"): 
                st.markdown(f'### {learnset[st.session_state.step][1]}')
        else:
            v.markdown(f'### {learnset[st.session_state.step][1]}')