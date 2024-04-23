
# opencv-python
import cv2
# mediapipe�˹����ܹ��߰�
import mediapipe as mp
# ��������
from tqdm import tqdm
# ʱ���
import time


# # ����ģ��

# ����solution
mp_hands = mp.solutions.hands
# ����ģ��
hands = mp_hands.Hands(static_image_mode=False,        # �Ǿ�̬ͼƬ����������Ƶ֡
                       max_num_hands=3,                # ����⼸ֻ��
                       min_detection_confidence=0.7,   # ���Ŷ���ֵ
                       min_tracking_confidence=0.5)    # ׷����ֵ
# �����ͼ����
mpDraw = mp.solutions.drawing_utils 


# # ����֡�ĺ���

def process_frame(img):
    
    # ��¼��֡��ʼ�����ʱ��
    start_time = time.time()
    
    # ��ȡͼ����
    h, w = img.shape[0], img.shape[1]

    # ˮƽ����תͼ��ʹͼ������������ʵ�����ֶ�Ӧ
    # ���� 1��ˮƽ��ת��0����ֱ��ת��-1��ˮƽ����ֱ����ת
    img = cv2.flip(img, 1)
    # BGRתRGB
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # ��RGBͼ������ģ�ͣ���ȡԤ����
    results = hands.process(img_RGB)

    if results.multi_hand_landmarks: # ����м�⵽��

        handness_str = ''
        index_finger_tip_str = ''
        for hand_idx in range(len(results.multi_hand_landmarks)):

            # ��ȡ���ֵ�21���ؼ�������
            hand_21 = results.multi_hand_landmarks[hand_idx]

            # ���ӻ��ؼ��㼰�Ǽ�����
            mpDraw.draw_landmarks(img, hand_21, mp_hands.HAND_CONNECTIONS)

            # ��¼��������Ϣ
            temp_handness = results.multi_handedness[hand_idx].classification[0].label
            handness_str += '{}:{} '.format(hand_idx, temp_handness)

            # ��ȡ��������������
            cz0 = hand_21.landmark[0].z

            for i in range(21): # �������ֵ�21���ؼ���

                # ��ȡ3D����
                cx = int(hand_21.landmark[i].x * w)
                cy = int(hand_21.landmark[i].y * h)
                cz = hand_21.landmark[i].z
                depth_z = cz0 - cz

                # ��Բ�İ뾶��ӳ��ȴ�С
                radius = max(int(6 * (1 + depth_z*5)), 0)

                if i == 0: # ����
                    img = cv2.circle(img,(cx,cy), radius, (0,0,255), -1)
                if i == 8: # ʳָָ��
                    img = cv2.circle(img,(cx,cy), radius, (235,206,135), -1)
                    # ��������������Ⱦ�����ʾ�ڻ�����
                    index_finger_tip_str += '{}:{:.2f} '.format(hand_idx, depth_z)
                if i in [1,5,9,13,17]: # ָ��
                    img = cv2.circle(img,(cx,cy), radius, (16,144,247), -1)
                if i in [2,6,10,14,18]: # ��һָ��
                    img = cv2.circle(img,(cx,cy), radius, (1,240,255), -1)
                if i in [3,7,11,15,19]: # �ڶ�ָ��
                    img = cv2.circle(img,(cx,cy), radius, (140,47,240), -1)
                if i in [4,12,16,20]: # ָ�⣨��ʳָָ�⣩
                    img = cv2.circle(img,(cx,cy), radius, (223,155,60), -1)

        scaler = 1
        img = cv2.putText(img, handness_str, (25 * scaler, 100 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1 * scaler, (255, 0, 255), 2 * scaler)
        img = cv2.putText(img, index_finger_tip_str, (25 * scaler, 150 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1 * scaler, (255, 0, 255), 2 * scaler)
        
        # ��¼��֡������ϵ�ʱ��
        end_time = time.time()
        # ����ÿ�봦��ͼ��֡��FPS
        FPS = 1/(end_time - start_time)

        # ��ͼ����дFPS��ֵ����������Ϊ��ͼƬ����ӵ����֣����Ͻ����꣬���壬�����С����ɫ�������ϸ
        scaler = 1
        img = cv2.putText(img, 'FPS  '+str(int(FPS)), (25 * scaler, 50 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1.25 * scaler, (255, 0, 255), 2 * scaler)
    return img


# # ��������ͷ��ȡÿ֡��ģ�壩

# ��������ͷ��֡ʵʱ����ģ��
# �����޸��κδ��룬ֻ���޸�process_frame��������
# ͬ���Ӻ��� 2021-7-8

# ����opencv-python
import cv2
import time

# ��ȡ����ͷ������0��ʾ��ȡϵͳĬ������ͷ
cap = cv2.VideoCapture(0)

# ��cap
cap.open(0)

# ����ѭ����ֱ��break������
while cap.isOpened():
    # ��ȡ����
    success, frame = cap.read()
    if not success:
        break
    
    ## !!!����֡����
    frame = process_frame(frame)
    
    # չʾ��������ͨ��ͼ��
    cv2.imshow('my_window', frame)

    if cv2.waitKey(1) in [ord('q'),27]: # �������ϵ�q��esc�˳�����Ӣ�����뷨�£�
        break
    
# �ر�����ͷ
cap.release()

# �ر�ͼ�񴰿�
cv2.destroyAllWindows()



