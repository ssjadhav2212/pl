public class alphaBeta {

    int MAX = 1000;
    int MIN = -1000;

    display d;

    public int minMax(int depth,int nodeNo,boolean isMax,int scores[],int h,int alpha,int beta)
    {
        if(depth == h)
        {
            System.out.println("currently evaluating node = "+scores[nodeNo]);
            d.setColor(nodeNo);
            return scores[nodeNo];

        }

        else if(isMax)
        {
            int best = MIN;
            for(int i=0;i<2;i++)
            {
                int val = minMax(depth+1,nodeNo*2+i,false,scores,h,alpha,beta);
                best = Math.max(val,best);
                alpha = Math.max(alpha,best);

                if(beta<=alpha)
                    break;
            }
            d.setText(best,depth,nodeNo*2,nodeNo*2+1);
            return best;
        }

        else
        {
            int best = MAX;
            for(int i=0;i<2;i++)
            {
                int val = minMax(depth+1,nodeNo*2+i,true,scores,h,alpha,beta);
                best = Math.min(best,val);
                beta = Math.min(beta,best);

                if(beta<=alpha)
                    break;
            }

            d.setText(best,depth,nodeNo*2,nodeNo*2+1);
            return best;
        }



    }

    int return_height(int n)
    {
        if(n==1)
            return 0;


        else
            return 1+return_height(n/2);
    }

    public static void main(String[] args) {

        System.out.println("For alpha beta");
        int scores[]={3, 5, 6,9,1,2,0,-1};

        alphaBeta ab = new alphaBeta();
        int height = ab.return_height(scores.length);

        ab.d = new display();

        ab.d.add_elements(scores,height);

        int result = ab.minMax(0,0,true,scores,height,ab.MIN,ab.MAX);

        System.out.println("optimal value is = "+result);


    }


}
