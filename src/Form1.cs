using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.IO.Ports;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Windows.Forms;


namespace intern_8ch
{


    public partial class Form1 : Form
    {
        //optitrack trigger 
        TcpClient tcpClient = null;
        NetworkStream clientStream;

        SerialPort sPort;
        static int channels = 1;             
        static int samples = 16;  
        int bufferSize = channels * samples * 9;
        
        static int degree = 1000;        // V -> mV
        static double VREF = 3.83; //4.5//3.83//3.3       // 1LSB= (2*VREF/Gain)/(2^(24))=+FS(2^(23))
        static byte STX = 0x81;
        static byte ETX = 0x82;
        static int PACKET_SIZE = 34;
        static uint Samplerate = 250;
        static uint BUFSIZE = Samplerate * 3;
        bool DataSaveFlag = false;
        bool feFlag = false;
        int count = -1;
        string thisdate, save_name, save_name_path, save_name_path1, save_name_path2;

        static Random random = new Random();
        System.Diagnostics.Stopwatch stopwch = new System.Diagnostics.Stopwatch();
        int trg = 0;        // V -> mV
        int[] idxFE = new int[11];        // V -> mV



        long[] INPUTDATA = new long[PACKET_SIZE + 1];

        long[] EMG_CH1_data_data = new long[BUFSIZE];
        long[] EMG_CH2_data_data = new long[BUFSIZE];
        long[] EMG_CH3_data_data = new long[BUFSIZE];
        long[] EMG_CH4_data_data = new long[BUFSIZE];
        long[] EMG_CH5_data_data = new long[BUFSIZE];
        long[] EMG_CH6_data_data = new long[BUFSIZE];
        long[] EMG_CH7_data_data = new long[BUFSIZE];
        long[] EMG_CH8_data_data = new long[BUFSIZE];

        double[] EMG_CH1_data_draw = new double[BUFSIZE];
        double[] EMG_CH2_data_draw = new double[BUFSIZE];
        double[] EMG_CH3_data_draw = new double[BUFSIZE];
        double[] EMG_CH4_data_draw = new double[BUFSIZE];
        double[] EMG_CH5_data_draw = new double[BUFSIZE];
        double[] EMG_CH6_data_draw = new double[BUFSIZE];
        double[] EMG_CH7_data_draw = new double[BUFSIZE];
        double[] EMG_CH8_data_draw = new double[BUFSIZE];


        long[] LPF_PPG_RED_data = new long[BUFSIZE];
        long[] PPG_RED_data = new long[BUFSIZE];



        private static List<int> GenerateRandom(int count)
        {
            // generate count random values.
            HashSet<int> candidates = new HashSet<int>();
            while (candidates.Count < count)
            {
                // May strike a duplicate.
                candidates.Add(random.Next());
            }

            // load them in to a list.
            List<int> result = new List<int>();
            result.AddRange(candidates);

            // shuffle the results:
            int i = result.Count;
            while (i > 1)
            {
                i--;
                int k = random.Next(i + 1);
                int value = result[k];
                result[k] = result[i];
                result[i] = value;
            }
            return result;
        }

        public Form1()
        {
            InitializeComponent();

            seri_OPEN.Enabled = true;
            seri_CLOSE.Enabled = false;
            CLOSE.Enabled = false;

            cbPORT.BeginUpdate();
            foreach (string comport in SerialPort.GetPortNames())
            {
                cbPORT.Items.Add(comport);
            }
            cbPORT.EndUpdate();

            CheckForIllegalCrossThreadCalls = false;

        }


        private void seri_OPEN_Click(object sender, EventArgs e)
        {
            try
            {
                // EMG 보드 시리얼 포트 여는 코드
                if (null == sPort)
                {
                    sPort = new SerialPort();
                    sPort.DataReceived += new SerialDataReceivedEventHandler(SPort_DataReceived);
                    sPort.PortName = cbPORT.SelectedItem.ToString();
                    sPort.BaudRate = Convert.ToInt32("115200");
                    sPort.DataBits = (int)8;
                    sPort.Parity = Parity.None;
                    sPort.StopBits = StopBits.One;
                    sPort.Open();
                    sPort.Write("T");                    
                }      
                
                if (sPort.IsOpen)
                {
                    seri_OPEN.Enabled = false;
                    seri_CLOSE.Enabled = true;
                }
                else
                {
                    seri_OPEN.Enabled = true;
                    seri_CLOSE.Enabled = false;

                }

                // TCP 포트 열고 스트림 받음
                if(tcpClient == null)
                {
                    tcpClient = new TcpClient();
                    tcpClient.Connect("localhost", 8888);
                    clientStream = tcpClient.GetStream();

                }


                // 표정 설정 하는 코드

                // repeat until all 8 valid random numbers are generated
                var counter = 0;
                do
                {
                    // generate a random number between 1 and 49
                    Random random = new Random();
                    var randomNumber = random.Next(1, idxFE.Length + 1);

                    // if the numbers array doesn't contain the random number
                    // add the random number to the array and increment the counter
                    if (Array.IndexOf(idxFE, randomNumber) == -1)
                    {
                        if (counter == 0)
                            idxFE[counter] = 9;
                        else
                            idxFE[counter] = randomNumber;
                        counter++;
                    }
                } while (counter < idxFE.Length);

                string strFEList = string.Format("INDEX OF FE: {0}", idxFE[count]);

                textBox1.Text = strFEList;

                //// display the first 7 numbers separated by comma
                //for (var i = 0; i < idxFE.Length - 1; i++)
                //{
                //    Console.Write(idxFE[i] + ",");
                //}

                //// display the last number which doesn't have a comma
                //Console.Write(idxFE[idxFE.Length - 1]);


            }
            catch (System.Exception ex)
            {
                MessageBox.Show(ex.Message);
            }


        }



        private void seri_CLOSE_Click(object sender, EventArgs e)
        {
            if (null != sPort)
            {
                if (sPort.IsOpen)
                {
                    sPort.Write("S");
                    sPort.Close();
                    sPort.Dispose();
                    sPort = null;
                }
            }

            seri_OPEN.Enabled = true;
            seri_CLOSE.Enabled = false;
        }



        void SPort_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            
            long EMG_CH1_data, EMG_CH2_data, EMG_CH3_data, EMG_CH4_data, EMG_CH5_data, EMG_CH6_data, EMG_CH7_data, EMG_CH8_data;

            

            while (sPort.BytesToRead > 0)
            {
                //optitrack trigger 
                byte marker = 0;
                if (tcpClient != null && clientStream != null)
                {
                    byte[] bytes = new byte[3];
                    clientStream.Read(bytes, 0, 3);
                    marker = bytes[1];

                }

                for (int ii = 0; ii < PACKET_SIZE; ii++)
                {
                    INPUTDATA[ii] = INPUTDATA[ii + 1];
                }

                long bybuf = sPort.ReadByte();
                INPUTDATA[PACKET_SIZE] = bybuf;


                if (INPUTDATA[0] == STX && INPUTDATA[PACKET_SIZE - 1] == ETX)
                {
                   

                    //DATA Recieve
                    EMG_CH1_data = ((int)INPUTDATA[1] << 21) + ((int)INPUTDATA[2] << 14) + ((int)INPUTDATA[3] << 7) + ((int)INPUTDATA[4]);
                    EMG_CH2_data = ((int)INPUTDATA[5] << 21) + ((int)INPUTDATA[6] << 14) + ((int)INPUTDATA[7] << 7) + ((int)INPUTDATA[8]);
                    EMG_CH3_data = ((int)INPUTDATA[9] << 21) + ((int)INPUTDATA[10] << 14) + ((int)INPUTDATA[11] << 7) + ((int)INPUTDATA[12]);
                    EMG_CH4_data = ((int)INPUTDATA[13] << 21) + ((int)INPUTDATA[14] << 14) + ((int)INPUTDATA[15] << 7) + ((int)INPUTDATA[16]);
                    EMG_CH5_data = ((int)INPUTDATA[17] << 21) + ((int)INPUTDATA[18] << 14) + ((int)INPUTDATA[19] << 7) + ((int)INPUTDATA[20]);
                    EMG_CH6_data = ((int)INPUTDATA[21] << 21) + ((int)INPUTDATA[22] << 14) + ((int)INPUTDATA[23] << 7) + ((int)INPUTDATA[24]);
                    EMG_CH7_data = ((int)INPUTDATA[25] << 21) + ((int)INPUTDATA[26] << 14) + ((int)INPUTDATA[27] << 7) + ((int)INPUTDATA[28]);
                    EMG_CH8_data = ((int)INPUTDATA[29] << 21) + ((int)INPUTDATA[30] << 14) + ((int)INPUTDATA[31] << 7) + ((int)INPUTDATA[32]);


                    //convert EEG Complement
                    EMG_CH1_data = (EMG_CH1_data & 0x7FFFFF) - (EMG_CH1_data & 0x800000);//CH_1_two = (CH_1 & 0x7fffff) - (CH_1 & 0x800000);
                    EMG_CH2_data = (EMG_CH2_data & 0x7FFFFF) - (EMG_CH2_data & 0x800000);
                    EMG_CH3_data = (EMG_CH3_data & 0x7FFFFF) - (EMG_CH3_data & 0x800000);//CH_1_two = (CH_1 & 0x7fffff) - (CH_1 & 0x800000);
                    EMG_CH4_data = (EMG_CH4_data & 0x7FFFFF) - (EMG_CH4_data & 0x800000);
                    EMG_CH5_data = (EMG_CH5_data & 0x7FFFFF) - (EMG_CH5_data & 0x800000);//CH_1_two = (CH_1 & 0x7fffff) - (CH_1 & 0x800000);
                    EMG_CH6_data = (EMG_CH6_data & 0x7FFFFF) - (EMG_CH6_data & 0x800000);
                    EMG_CH7_data = (EMG_CH7_data & 0x7FFFFF) - (EMG_CH7_data & 0x800000);//CH_1_two = (CH_1 & 0x7fffff) - (CH_1 & 0x800000);
                    EMG_CH8_data = (EMG_CH8_data & 0x7FFFFF) - (EMG_CH8_data & 0x800000);

                    //convert EEG voltage 24 gain

                    EMG_CH1_data = (long)(EMG_CH1_data * VREF * degree) / (8388607);
                    EMG_CH2_data = (long)(EMG_CH2_data * VREF * degree) / (8388607);
                    EMG_CH3_data = (long)(EMG_CH3_data * VREF * degree) / (8388607);
                    EMG_CH4_data = (long)(EMG_CH4_data * VREF * degree) / (8388607);
                    EMG_CH5_data = (long)(EMG_CH5_data * VREF * degree) / (8388607);
                    EMG_CH6_data = (long)(EMG_CH6_data * VREF * degree) / (8388607);
                    EMG_CH7_data = (long)(EMG_CH7_data * VREF * degree) / (8388607);
                    EMG_CH8_data = (long)(EMG_CH8_data * VREF * degree) / (8388607);


                    //Buffering
                    for (int j = 0; j < (BUFSIZE - 1); j++)
                    {

                        EMG_CH1_data_data[j] = EMG_CH1_data_data[j + 1];
                        EMG_CH2_data_data[j] = EMG_CH2_data_data[j + 1];
                        EMG_CH3_data_data[j] = EMG_CH3_data_data[j + 1];
                        EMG_CH4_data_data[j] = EMG_CH4_data_data[j + 1];
                        EMG_CH5_data_data[j] = EMG_CH5_data_data[j + 1];
                        EMG_CH6_data_data[j] = EMG_CH6_data_data[j + 1];
                        EMG_CH7_data_data[j] = EMG_CH7_data_data[j + 1];
                        EMG_CH8_data_data[j] = EMG_CH8_data_data[j + 1];


                    }


                    EMG_CH1_data_data[BUFSIZE - 1] = EMG_CH1_data;
                    EMG_CH2_data_data[BUFSIZE - 1] = EMG_CH2_data;
                    EMG_CH3_data_data[BUFSIZE - 1] = EMG_CH3_data;
                    EMG_CH4_data_data[BUFSIZE - 1] = EMG_CH4_data;
                    EMG_CH5_data_data[BUFSIZE - 1] = EMG_CH5_data;
                    EMG_CH6_data_data[BUFSIZE - 1] = EMG_CH6_data;
                    EMG_CH7_data_data[BUFSIZE - 1] = EMG_CH7_data;
                    EMG_CH8_data_data[BUFSIZE - 1] = EMG_CH8_data;

                    if (DataSaveFlag)
                    {
                        int trg;

                        if ((count >= 0 && count < 11) && (stopwch.ElapsedMilliseconds >= 3000))
                            trg = idxFE[count];
                        else if (count >=11)
                            trg = 0;
                        else
                            trg = 0;


                        
                        string dataline = string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}", (float)EMG_CH1_data, (float)EMG_CH2_data, (float)EMG_CH3_data, (float)EMG_CH4_data, (float)EMG_CH5_data, (float)EMG_CH6_data, (float)EMG_CH7_data, (float)EMG_CH8_data, trg, marker);
                        Console.WriteLine(dataline);

                        StreamWriter sw = new StreamWriter(save_name, true);
                        sw.WriteLine(dataline);
                        sw.Close();


                    }

                    string str;

                    if (stopwch.ElapsedMilliseconds >= 1000 && stopwch.ElapsedMilliseconds < 2000)
                    {
                        str = "Wait (2 s left)";
                        textBox1.Text = str;
                    }
                    else if (stopwch.ElapsedMilliseconds >= 2000 && stopwch.ElapsedMilliseconds < 3000)
                    {
                        str = "Wait (1 s left)";
                        textBox1.Text = str;
                    }
                    else if (stopwch.ElapsedMilliseconds >= 3000 && stopwch.ElapsedMilliseconds < 4000)
                    {
                        str = "Make a Facial Expression (1 s)";
                        textBox1.Text = str;
                    }

                    if (feFlag && stopwch.ElapsedMilliseconds >= 3000)
                    {
                        

                        if (stopwch.ElapsedMilliseconds >= 4000 && stopwch.ElapsedMilliseconds < 5000)
                        {
                            str = "Make a Facial Expression (2 s)";
                            textBox1.Text = str;
                        }
                        else if (stopwch.ElapsedMilliseconds >= 5000 && stopwch.ElapsedMilliseconds < 6000)
                        {
                            str = "Make a Facial Expression (3 s)";
                            textBox1.Text = str;
                        }
                        else if (stopwch.ElapsedMilliseconds >= 6000 && stopwch.ElapsedMilliseconds < 7000)
                        {
                            str = "Rest";
                            textBox1.Text = str;
                            feFlag = false;
                            StartnNext.Enabled = true;
                            stopwch.Reset();
                        }


                    }
                }
            }

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {


        }

        private void StartnNext_Click(object sender, EventArgs e)
        {
            
            feFlag = true;
            count++;
            StartnNext.Enabled = false;
            // 실험 끝났을 때
            if (count == 11)
            {
                //DataSaveFlag = false;
                timer1.Stop();
                seri_CLOSE.Enabled = false;
                StartnNext.Enabled = false;
            }
            else
            {
                // 사진 파일 선택
                string strFormattedDate = string.Format("resize_{0}.png", idxFE[count]);
                string file_fullpath1 = System.IO.Path.Combine(System.IO.Directory.GetParent(Application.StartupPath).FullName, "pics", strFormattedDate);

                // 사진 바꾸기
                pictureBox1.Image = Bitmap.FromFile(file_fullpath1);
                pictureBox1.Visible = true; ;
                //pictureBox1.ImageLocation.Normalize();


                // 시간 저장 및 초기화
                if (!stopwch.IsRunning)
                    stopwch.Start();
            }
            

        }

        private void On_timer1(object sender, EventArgs e)
        {


            for (int i = 0; i < BUFSIZE; i++)
            {
                EMG_CH1_data_draw[i] = EMG_CH1_data_data[i];
                EMG_CH2_data_draw[i] = EMG_CH2_data_data[i];
                EMG_CH3_data_draw[i] = EMG_CH3_data_data[i];
                EMG_CH4_data_draw[i] = EMG_CH4_data_data[i];
                EMG_CH5_data_draw[i] = EMG_CH5_data_data[i];
                EMG_CH6_data_draw[i] = EMG_CH6_data_data[i];
                EMG_CH7_data_draw[i] = EMG_CH7_data_data[i];
                EMG_CH8_data_draw[i] = EMG_CH8_data_data[i];

            }

            scope1.Channels[0].Data.SetYData(EMG_CH1_data_draw, 0, BUFSIZE);
            scope2.Channels[0].Data.SetYData(EMG_CH2_data_draw, 0, BUFSIZE);
            scope3.Channels[0].Data.SetYData(EMG_CH3_data_draw, 0, BUFSIZE);
            scope4.Channels[0].Data.SetYData(EMG_CH4_data_draw, 0, BUFSIZE);
            scope5.Channels[0].Data.SetYData(EMG_CH5_data_draw, 0, BUFSIZE);
            scope6.Channels[0].Data.SetYData(EMG_CH6_data_draw, 0, BUFSIZE);
            scope7.Channels[0].Data.SetYData(EMG_CH7_data_draw, 0, BUFSIZE);
            scope8.Channels[0].Data.SetYData(EMG_CH8_data_draw, 0, BUFSIZE);
        }

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            if (null != sPort)
            {
                if (sPort.IsOpen)
                {
                    sPort.Close();
                    sPort.Dispose();
                    sPort = null;
                }
            }
        }

        private void SAVE_Click(object sender, EventArgs e)
        {
            SAVE.Enabled = false;
            CLOSE.Enabled = true;

            thisdate = DateTime.Now.ToString("yyyy년MM월dd일hh시mm분ss초");
            save_name = thisdate + ".txt";
            FileStream fsa = File.Create(save_name);
            fsa.Close();
            DataSaveFlag = true;
        }

        private void CLOSE_Click(object sender, EventArgs e)
        {
            if (DataSaveFlag)
            {
                DataSaveFlag = false;
                CLOSE.Enabled = false;
                SAVE.Enabled = false;
                seri_CLOSE.Enabled = false;
                StreamWriter sw = new StreamWriter(save_name, true);
                thisdate = DateTime.Now.ToString("yyyy년MM월dd일hh시mm분ss초");
                sw.WriteLine("End Time : " + thisdate);
                sw.Close();
            }

        }
    }
}

