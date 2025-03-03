# AWS Security Concepts

![image.png](images/image.png)

Securing AWS EC2 instances is crucial for safeguarding your data, applications, and overall cloud infrastructure. Unsecured instances can be exploited by attackers, leading to data breaches, service disruptions, and financial losses. By implementing robust security measures, you can protect your sensitive information, maintain operational continuity, and comply with relevant regulations.

Following I am providing some of the concepts to securing the EC2 instance in AWS Environment -

1. Using VPC (subnets, security groups, route tables and internet gateway)
2. Implementing NACL
3.  Using Elastic Load Balancer
4. Using AutoScaling Group
5. Integrate Load Balancer with AutoScaling Group
6. Implementing Web Application Firewall
7. Using AWS Shield Standard and Advanced
8. Implementing AWS GuardDuty
9. Working with AWS Security Hub
10. Implementing TLS Termination (AWS ACM)
11. Enable logging via AWS CloudTrail
12. Managing Secrets using AWS Secret Manager
13. Enabling Encryption using AWS KMS
14. Enabling Automatic Backup Amazon Data Lifecycle Manager
15. Setting up Alerts using AWS CloudWatch and SNS
16. Managing Resource access Permissions using IAM Roles

# Concept 1 : Using VPC (subnets, security groups, route tables and internet gateway)

Amazon Virtual Private Cloud (VPC) is a service that lets you launch AWS resources in a logically isolated virtual network. A VPC is essential for secure, controlled, and scalable deployment of cloud-based applications.

Some important points regarding VPC are following -

1. We can create **5 VPCs** per region and **200 Subnets** in a VPC.
2. AWS provides **5 Elastic IP addresses** per region by default.
3. More VPC’s and elastic ip’s are possible but for that we need to request AWS.
4. When we create a VPC then 3 things are automatically made i.e. **DHCP, NACL and SG**. (Dynamic Host Control Protocol, Network Access Control List and Security Group).

## Steps to create a VPC

## Step 1: Log in to the AWS Management Console

1. Navigate to the [AWS Management Console](https://aws.amazon.com/console/).
2. Search for **VPC** in the search bar and select **VPC Dashboard**.

## Step 2: Create a New VPC

1. In the VPC Dashboard, go to **Your VPCs**.
2. Click **Create VPC**.
3. Provide the following details:
    - **Name Tag:** Assign a name for your VPC (e.g., "MyCustomVPC").
    - **IPv4 CIDR Block:** Specify the range of IP addresses (e.g., `10.0.0.0/16`). (You must be aware about the Classes of IP Address to choose correct CIRD for your VPC)
    - **IPv6 CIDR Block (optional):** Enable IPv6 if needed, or leave it disabled.
    - **Tenancy:** Choose "Default" unless you need "Dedicated" (higher cost).

**Class**

---

**Address Range**

**Default Subnet Mask**

**Purpose**

**Hosts per Network**

| A | `1.0.0.0 - 126.255.255.255` | `255.0.0.0` (/8) | Large networks | 16,777,214 |
| --- | --- | --- | --- | --- |
| B | `128.0.0.0 - 191.255.255.255` | `255.255.0.0` (/16) | Medium-sized networks | 65,534 |
| C | `192.0.0.0 - 223.255.255.255` | `255.255.255.0` (/24) | Small networks | 254 |
| D | `224.0.0.0 - 239.255.255.255` | Not applicable | Multicast applications | Not applicable |
| E | `240.0.0.0 - 255.255.255.255` | Not applicable | Experimental use | Not applicable |
1. Click Create VPC.

![image.png](images/image%201.png)

![image.png](images/image%202.png)

![image.png](images/image%203.png)

## Step 3: Create Subnets

Subnet allows you to segment the VPC for organizing resources.

1. Go to **Subnets** in the VPC Dashboard.
2. Click **Create Subnet.**
3. Provide the following details:
    - **Name Tag:** Name the subnet (e.g., "PublicSubnet1" or "PrivateSubnet1").
    - **VPC ID:** Select the VPC you just created.
    - **Availability Zone:** Choose an Availability Zone (e.g., `us-east-1a`).
    - **IPv4 CIDR Block:** Specify a range within the VPC (e.g., `10.0.1.0/24`).
4. Click **Create Subnet**.
5. Repeat these steps to create additional subnets:
    - **Public Subnets:** For internet-facing resources (e.g., web servers).
    - **Private Subnets:** For backend resources (e.g., databases).

![image.png](images/image%204.png)

## Step 4: Create an Internet Gateway

An Internet Gateway (IGW) allows resources in your public subnets to access the internet.

1. Go to **Internet Gateways** in the VPC Dashboard.
2. Click **Create Internet Gateway**.
3. Provide a **Name Tag** (e.g., "MyCustomIGW") and click **Create**.
4. Select the IGW and click **Actions** > **Attach to VPC**.
5. Select your VPC and click **Attach Internet Gateway**.

![image.png](images/image%205.png)

![image.png](images/image%206.png)

![image.png](images/image%207.png)

![image.png](images/image%208.png)

## Step 5: Create Route Tables

Route tables determine how traffic is routed within your VPC. When a subnet is created then it’s a good practice to create a corresponding route table with a subnet and associate it. It will be helpful to make a subnet public or private.

### Create a Route Table for Public Subnets:

1. Go to **Route Tables** in the VPC Dashboard.
2. Click **Create Route Table**.
3. Provide a **Name Tag** (e.g., "PublicRouteTable").
4. Select your VPC and click **Create**.
5. Select the route table you created and go to the **Routes** tab.
6. Click **Edit Routes**:
    - **Destination:** `0.0.0.0/0` (default route for all outbound internet traffic).
    - **Target:** Select the Internet Gateway you created.
7. Click **Save Routes**.

![image.png](images/image%209.png)

![image.png](images/image%2010.png)

### Associate Public Subnets with Public Route Table:

1. Go to the **Subnet Associations** tab of the public route table.
2. Click **Edit Subnet Associations**.
3. Select the public subnets and click **Save Associations**.

![image.png](images/image%2011.png)

### Configure Route Table for Private Subnets:

1. Create a route table for private subnet in similar way without adding an entry of Internet Gateway.
2. Then do the subnet association.

## Step 6: Configure Security Groups

Security groups act as virtual firewalls for your instances.

1. Go to **Security Groups** in the VPC Dashboard.
2. Click **Create Security Group**.
3. Provide the following details:
    - **Name Tag:** Name the security group (e.g., "PublicSG" or "PrivateSG").
    - **Description:** Provide a description.
    - **VPC:** Select your VPC.
4. Configure **Inbound Rules**:
    - For PublicSG:
        - Allow HTTP (port 80) and HTTPS (port 443).
        - Allow SSH (port 22) from a trusted IP.
    - For PrivateSG:
        - Allow database traffic (e.g., port 3306 for MySQL) only from the PublicSG.
5. Configure **Outbound Rules**:
    - Allow all traffic by default (you can restrict this if needed).

![image.png](images/image%2012.png)

![image.png](images/image%2013.png)

![image.png](images/image%2014.png)

![image.png](images/image%2015.png)

# Concept 2: Implementing NACL

Network Access Control Lists (NACLs) in AWS are used to control inbound and outbound traffic at the subnet level. They act as a firewall for controlling traffic based on rules that allow or deny traffic. NACLs are stateless, it means if you allow inbound traffic for a port then you must also explicitly allow outbound responses for same port. Unlike security groups, NACLs allow you to define explicit deny rules to block specific traffic. This is particularly useful for Blocking malicious IP addresses and Restricting access to certain ports or protocols.

## Step 1: Access the VPC Dashboard

1. Log in to your [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to **VPC Dashboard**.
3. In the left-hand menu, click on **Network ACLs** under **Security**.

## Step 2: Create a New NACL

1. **Create network ACL**:
    - From UI, Click Create network ACL
    - Enter a name for the NACL (optional but recommended).
    - Select the VPC where the NACL will be associated.
2. **Click Create**.

![image.png](images/image%2016.png)

![image.png](images/image%2017.png)

## Step 3: Associate the NACL with a Subnet

1. After creating the NACL, select it from the list.
2. Go to the **Subnet associations** tab.
3. Click **Edit subnet associations**.
4. Select the subnet(s) where you want to apply this NACL.
5. Click **Save**.

![image.png](images/image%2018.png)

![image.png](images/image%2019.png)

![image.png](images/image%2020.png)

## Step 4: Define Inbound and Outbound Rules

1. Select the NACL from the list.
2. Go to the **Inbound rules** or **Outbound rules** tab.
3. Click **Edit inbound rules** or **Edit outbound rules**.

### Add Rules:

- Each rule consists of:
    - **Rule Number**: Determines the order in which rules are evaluated (lowest number first).
    - **Type**: The type of traffic (e.g., HTTP, SSH, Custom Protocol).
    - **Protocol**: TCP, UDP, or ICMP (or all protocols with `1`).
    - **Port Range**: The range of ports (e.g., 80 for HTTP, 22 for SSH).
    - **Source/Destination**:
        - For inbound rules, specify the source (e.g., `0.0.0.0/0` for all IPs).
        - For outbound rules, specify the destination.
    - **Allow/Deny**: Choose whether to allow or deny the traffic.
1. Click **Save changes** after adding rules.

![image.png](images/image%2021.png)

![image.png](images/image%2022.png)

![image.png](images/image%2023.png)

![image.png](images/image%2024.png)

# Concept 3: Using Elastic Load Balancer

Setting up an Elastic Load Balancer (ELB) in AWS involves creating the load balancer, configuring its settings, and attaching backend resources like EC2 instances.

## Step-by-step guide to set up an Elastic Load Balancer

## Step 1: Log in to the AWS Management Console

1. Go to the [AWS Management Console](https://aws.amazon.com/console/).
2. Search for **EC2** in the search bar and navigate to the **EC2 Dashboard**.
3. From the left-hand menu, select **Load Balancers** under **Load Balancing**.

## Step 2: Choose the Type of Load Balancer

AWS offers three types of ELBs:

1. Click **Create Load Balancer**.
2. Select the load balancer type that suits your needs (e.g., Application Load Balancer for web applications).
    1. **Application Load Balancer (ALB):** For HTTP/HTTPS traffic with advanced routing capabilities.
    2. **Network Load Balancer (NLB):** For TCP, TLS, or UDP traffic requiring high throughput and low latency.
    3. **Classic Load Balancer (CLB):** Legacy option for basic HTTP/HTTPS or TCP traffic.

For our implementation purpose, we are selecting Application Load Balancer

## **Step 3: Configure Basic Load Balancer Settings**

1. **Basic Configuration:**
    - **Name:** Enter a unique name for your ALB (e.g., `MyALB`).
    - **Scheme:**
        - Choose **Internet-facing** for public-facing applications.
        - Choose **Internal** for private applications.
    - **IP Address Type:** Select IPv4 or dual-stack (IPv4 and IPv6).
2. **Network Mapping:**
    - Choose the VPC where your resources are located.
    - Select the Availability Zones and subnets to deploy the load balancer.

![image.png](images/image%2025.png)

![image.png](images/image%2026.png)

![image.png](images/image%2027.png)

![image.png](images/image%2028.png)

## Step 4: Set Up a Target Group:

You can create multiple targets if your application supports multiple protocols.

1. Click **Create Target Group**:
    - **Name:** Enter a name for the target group (e.g., `MyTargetGroup`).
    - **Protocol:** Choose HTTP, HTTPS, or TCP based on your application.
    - **Target Type:** Choose from:
        - **Instances:** For EC2 instances.
        - **IP Addresses:** For resources using private IPs.
        - **Lambda Functions:** To route requests to Lambda.
    - **Port:** Specify the port on which your application listens (e.g., `80`).
2. Configure health check settings:
    - **Protocol:** HTTP or HTTPS.
    - **Path:** Specify the health check endpoint (e.g., `/health`).
    - **Healthy/Unhealthy Thresholds:** Set the number of successful or failed checks before marking a target as healthy/unhealthy.
    - Adjust the interval, timeout, and success codes as needed.
3. Register Targets:
    - Select the resources (e.g., EC2 instances) to add to the target group.
    - Click **Include as Pending Below** and then **Register Targets**.

![image.png](images/image%2029.png)

![image.png](images/image%2030.png)

![image.png](images/image%2031.png)

## **Step 5: Configure Listeners:**

Listeners define how the load balancer listens for incoming traffic. You should be aware that it is mandatory to add at least 2 public subnets (present in differnet AZ’s)

1. Click **Add Listener**:
    - Choose a **Protocol** (e.g., HTTP or HTTPS).
    - Specify a **Port** (e.g., `80` for HTTP or `443` for HTTPS).
2. If using HTTPS:
    - Set up an SSL certificate (AWS Certificate Manager (ACM) or upload your certificate).
    - Select a security policy.

![image.png](images/image%2032.png)

## Step 6: Configure Security Groups

While creating application load balancer.

1. Assign a security group to the load balancer:
    - Open the **Load Balancer Security Group** page.
    - Create or select a security group that allows inbound traffic on the listener ports (e.g., HTTP/80 or HTTPS/443).
2. Ensure backend EC2 instances allow traffic from the load balancer’s security group.

## Step 7: Add Tags (Optional)

1. Add key-value tags to organize and manage your load balancer (e.g., `Environment=Production`).
2. Click **Next** or **Skip** if not adding tags.

## Step 8: Review and Create the Load Balancer

1. Review all the settings to ensure correctness:
    - Load balancer name, type, scheme, listeners, target group, and security groups.
2. Click **Create Load Balancer**.
3. Wait for the load balancer to be provisioned (status: **Active**).

![image.png](images/image%2033.png)

## Step 9: Test Your Load Balancer

Note the DNS name of the load balancer from the **Description** tab. Example: `my-alb-1234567890.us-east-1.elb.amazonaws.com`.

1. Test the DNS name in a browser or use tools like `curl` or Postman to verify connectivity.
2. Ensure traffic is distributed evenly among registered targets.

![image.png](images/image%2034.png)

![image.png](images/image%2035.png)

![image.png](images/image%2036.png)

![image.png](images/image%2037.png)

![image.png](images/image%2038.png)

# Concept 4: Using AutoScaling Group

Creating an **Auto Scaling Group (ASG)** in AWS involves defining a launch template or configuration, setting up scaling policies, and configuring the group to distribute and manage EC2 instances dynamically. Don’t forget to provide the instance name through tags and enabling auto-assigned public ip.

Here I already have a EC2 instance running in AWS. I am just replicating same server to set up autoscaling group. Make sure that your start up script must be ready which should run automatically at the start of server to make it up.

## Step 1: Consider your Source Machine

1. Open the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to **EC2** by searching for it in the services search bar.
3. Go to your server and check whether it is running properly.

![image.png](images/image%2039.png)

![image.png](images/image%2040.png)

## Step 2: Prepare your own Custome AMI

Now we are going to create an image from our source machine, which will be useful to create the template.

1. **Navigate to EC2 Dashboard**:
    - Open the [AWS Management Console](https://aws.amazon.com/console/) and go to the **EC2 Dashboard**.
2. **Select the Instance**:
    - Under **Instances**, locate and select the EC2 instance you want to create an AMI from.
3. **Stop the Instance (Optional)**:
    - Although not mandatory, it's a good practice to stop the instance to ensure that data on the root volume is in a consistent state before creating the AMI.
    - You can stop the instance by selecting it and clicking on **Instance state > Stop instance**.
    
    ![image.png](images/image%2041.png)
    
4. **Create Image**:
    - With the instance selected, click on **Actions > Image and templates > Create Image**.
    
    ![image.png](images/image%2042.png)
    
5. **Configure the Image**:
    - **Image name**: Provide a descriptive name for your AMI.
    - **Image description**: Optionally, add a description to help you identify the AMI later.
    - **Instance volumes**: Review and customize the volumes to include in the AMI. You can adjust the size of the root volume or add additional volumes if needed.
    
    ![image.png](images/image%2043.png)
    
6. **Create Image**:
    - Click on the **Create Image** button to start the process. AWS will create a snapshot of the root volume and additional volumes (if any) to generate the AMI.
    
    ![image.png](images/image%2044.png)
    
7. **Monitor AMI Creation**:
    - Go to the **AMIs** section in the EC2 Dashboard to monitor the status of your AMI. It will be in a `pending` state initially and change to `available` once it's ready.

## Step 3: Create a Launch Template

1. From the **EC2 Dashboard**, click **Launch Templates** in the left-hand menu.
2. Click **Create Launch Template**.

![image.png](images/image%2045.png)

1. Fill in the required fields:
    - **Template Name**: Provide a descriptive name (e.g., `MyLaunchTemplate`).
    - **Version Description**: Optional description for versioning purposes.
    - **AMI ID**: Select an your custom Amazon Machine Image (AMI) for the instances that you had created from you nginx server.
    - **Instance Type**: Choose an instance type (e.g., `t2.micro`) or that one which satisfies the requirement of your project.
    - **Key Pair**: Select an existing key pair or create a new one for SSH access (if neded)
    - **Network settings**:
        - Select the subnet (or puplic subnet) where you want to set up your machine.
        - Select one or more security groups to define instance network rules, that is required by your application.
        - Go to Advanced Network Configuration and set auto-assign public ip as enabled.
    - **Storage**: Configure the storage (e.g., 8 GiB for a general-purpose SSD) or leave it as default
    - **Advanced Details**: Optionally, configure additional details like IAM roles, user data scripts, or purchasing options if you prefer.
2. Click **Create Launch Template**.

![image.png](images/image%2046.png)

![image.png](images/image%2047.png)

![image.png](images/image%2048.png)

![image.png](images/image%2049.png)

![image.png](images/image%2050.png)

![image.png](images/image%2051.png)

## Step 4: Create an Auto Scaling Group

1. **Navigate to Auto Scaling Groups**:
    - In the EC2 Dashboard, scroll down and click on **Auto Scaling Groups** under **Auto Scaling**.
2. **Create Auto Scaling Group**:
    - Click **Create Auto Scaling Group**.
3. **Choose Launch Template**:
    - **Name**: Provide a name for the Auto Scaling group. (MyASG)
    - **Launch Template**: Select the launch template created earlier. You can choose a specific version or the default version.
    
    ![image.png](images/image%2052.png)
    
4. **Customize your Network setting**:
    - Choose your VPC , AZ and subnet where you want to span you AutoScaling Group. Ensure the have multiple Availability Zones for high availability.
    - **Minimum Capacity**: Set the minimum number of instances (e.g., 1).
    - **Maximum Capacity**: Set the maximum number of instances (e.g., 5).
    
    ![image.png](images/image%2053.png)
    
5. Configure Group Size and Scaling Policies:
    1. **Desired Capacity**: Specify the number of instances you want to run initially (e.g., 3).
    2. **Minimum Capacity**: Set the minimum number of instances (e.g., 1).
    3. **Maximum Capacity**: Set the maximum number of instances (e.g., 5).
6. **Set Scaling Policies**: Unselect the option of “No Scaling Policies”.
    - **Target Tracking Scaling**: Automatically scale based on metrics like CPU usage.
    - **Step Scaling**: Scale based on defined thresholds.
    - **Schedule Scaling**: Scale at specific times.
7. **Configure Notifications (Optional)**:
    - Add notifications for scaling activities if needed (e.g., send an email via SNS).
8. **Add Tags:**
    - Add tags to the Auto Scaling group and the instances it creates. ( Here I set Name tag with value “instance from MyASG”)
9. **Review and Create**:
    - Review your configuration and click **Create Auto Scaling Group**.

## Step 5: Verify Auto Scaling Group

1. Navigate back to the **Auto Scaling Groups** page.
2. Check the status of your group to ensure it is active.
3. Confirm that the desired number of instances is launched and distributed across the specified subnets.
4. Copy the public IP address of your instance and check whether they are working or not.

![image.png](images/image%2054.png)

![image.png](images/image%2055.png)

# Concept 5: Integrate Load Balancer with AutoScaling Group

We are going to configure an Application Load Balancer and AutoScaling group such that we will use the DNS name of Application Load balaner and instance created by Autoscaling group will be used as Targets.

## Step 1: Make Target Group as with no targets.

We had already created a target group and attached to Application Load Balancer. This time we are going to set the targets as instances created by AutoScaling Group so for that, remove all the targest if any existing

1. **Navigate to Load Balancers**:
    - In the EC2 Dashboard, under **Load Balancing**, click **Target Groups**.
2. **Remove Targets**:
    - Scroll down and go to targets tab
    - Select all the targets and click on de register button.

![image.png](images/image%2056.png)

## Step 2: Integrate AutoScaling group with Target Group

1. **Navigate to Auto Scaling Groups**:
    - In the EC2 Dashboard, click on **Auto Scaling Groups**.
2. **Set your target group**
    - Click on Integrations tab after entering into your AutoScaling group
    - Click on edit button and check the option “Application, Network or Gateway Load Balancer target groups”
    - Click on drop down and choose the target group that is associated to your respective Application Load Balancer.

![image.png](images/image%2057.png)

![image.png](images/image%2058.png)

![image.png](images/image%2059.png)

## Step 3: Check your Application

1. **Check your Target groups**
    - In the EC2 Dashboard, under **Load Balancing**, click **Target Groups**.
    - Go to your Target group
    - You will be noticing registered targets will start reflecting the instances created by AutoScaling group.
2. **Check Application Load Balancer**
    - select **Load Balancers** under **Load Balancing** from EC2 Dashboard
    - go to your Application Load Balancer and copy the DNS name.
    - Then paste the DNS name to new tab and see the working of your application.

![image.png](images/image%2060.png)

![image.png](images/image%2061.png)

# Concept 6: Implementing Web Application Firewall

In AWS WAF, rules are evaluated in order of their priority. Lower priority numbers have higher importance. Following we are just observing that if we allow a particular IP address and deny all other IP’s (unknown), then how does it looks like on dashbord (counts and matrices). Here I am just allowing IP address of my personal laptop and deny all other. Then I will hit the URL (and refresh page) number of time to generate a traffic, in both of my laptop and mobile. Requests from my laptops were allowed and webpage will be displayed but webpage from my phone will be forbidden.

To implement AWS WAF (Web Application Firewall) for an Application Load Balancer (ALB) in AWS, and perform tasks like creating an IP set, adding rules to count requests, and viewing metrics in CloudWatch, follow the detailed steps below:

## Step 1: Create an IP Set to Allow and Count Requests

An **IP Set** allows you to define a set of IP addresses. You can use this IP set to either allow or block specific IP addresses.

1. **Log in to AWS Management Console**.
2. **Navigate to AWS WAF & Shield** service:
    - In the AWS Management Console, search for and select **WAF & Shield** under **Security, Identity, & Compliance**.
3. **Create an IP Set**:
    - In the left sidebar, click on **IP sets**.
    - Click **Create IP set**.
    - Name the IP set (e.g., `AllowedIPs`).
    - Choose the region (typically, choose the region where your ALB is located).
    - For **IP address version**, select either **IPv4** or **IPv6**, depending on your use case.
    - Click **Next**.
4. **Add IP Addresses**:
    - Add the specific IP addresses or IP ranges (CIDR blocks) that you want to allow your own IP
    - After adding, click **Create IP set**.

![image.png](images/image%2062.png)

![image.png](images/image%2063.png)

![image.png](images/image%2064.png)

## Step 2: Create a WAF Web ACL

A **Web ACL (Access Control List)** is a set of rules that define how to handle web requests. You will apply this ACL to your ALB to protect it.

1. In the **WAF & Shield** dashboard, click on **Web ACLs** in the left sidebar.
2. Click **Create Web ACL**.
3. Provide a name for your Web ACL (e.g., `MyWebACL`).
4. **Choose the region** (the same as where your ALB is deployed).
5. Under **Resources to associate**, choose **Application Load Balancer**. We are attaching same load balancer which we had created just above.
6. Click **Next**.

![image.png](images/image%2065.png)

![image.png](images/image%2066.png)

![image.png](images/image%2067.png)

## Step 3: Create a Rule to Count Requests Using the IP Set

Now, you need to create a rule that counts requests from the IP addresses in the IP set you created earlier.

1. **In the Web ACL Creation Wizard**, after selecting the resources to associate, click on **Add rule**.
2. Under **Rule type**, select **IP set match**.
3. Name the rule (e.g., `allow-rule`).
4. Under **IP set**, select the IP set you created in Step 1 (e.g., `myIPSet`).
5. Choose the action for this rule:
    - For testing purpose, we are choosing allow.
6. Click **Add rule**.

![image.png](images/image%2068.png)

![image.png](images/image%2069.png)

## Step 4: Set the Default Action to Deny

The **default action** for a Web ACL defines what happens to requests that don’t match any rules.

1. Scroll to the **Default action** section in the Web ACL creation wizard.
2. Select **Deny**.
3. Click **Next** and then click **Create Web ACL**.

![image.png](images/image%2070.png)

## Step 5: Test the ACL in Action - testing IP Set Matching and Counting

After applying the WAF ACL to the ALB, you need to verify whether it's working as expected.

1. **Send Requests**:
    - Send HTTP requests to your ALB from IPs in the IP set (to be counted).
    - Send requests from IPs outside of the IP set (to be denied).
2. **Monitor Metrics**:
    - The **counting** action will track requests that match the IP set.

![image.png](images/image%2071.png)

![image.png](images/image%2072.png)

![image.png](images/image%2073.png)

## Step 6: View Metrics in CloudWatch - View CloudWatch Metrics for AWS WAF

AWS WAF integrates with CloudWatch to provide detailed metrics for your Web ACL, including the number of requests counted, allowed, blocked, and more.

1. **Navigate to CloudWatch**:
    - In the AWS Management Console, search for and select **CloudWatch**.
2. **View WAF Metrics**:
    - In the left sidebar, select **Metrics**.
    - Under **Browse**, click on **WAF**.
    - You’ll see a list of metrics for each Web ACL.
    - Metrics include:
        - **AllowedRequests**: Requests allowed by your Web ACL.
        - **BlockedRequests**: Requests blocked by your Web ACL.
        - **CountedRequests**: Requests that are counted by your rule (like the one we created).
3. **Select Metrics**:
    - Click on the metrics you want to monitor.
    - You can create CloudWatch Dashboards for a more visual representation of the data.
    - Set alarms to notify you when certain thresholds are reached (e.g., when a certain number of requests have been counted).
    
    ![image.png](images/image%2074.png)
    
    ![image.png](images/image%2075.png)
    
    ![image.png](images/image%2076.png)
    
4. See Matrix from WAF itselef:
    1. Go to WAF Dashboard and go to your Web ACL
    2. From Traffic Overview you can see summary of your requests like number of Total requests, Blocked Requests, Allowed Requests, etc.
    3. You can also go to Sampled Request tab, there you will be able to see the graph based on your Requests

![image.png](images/image%2077.png)

![image.png](images/image%2078.png)

# Concept 7: Using AWS Shield Standard and Advanced

**AWS Shield Standard** is automatically enabled for most AWS resources by default, providing protection against common and larger-scale **Distributed Denial of Service (DDoS)** attacks. This service requires no manual configuration or additional cost to activate.

Here I did not implemented AWS Shield Standard as it is alredy enabled when we use services like Cloudfront, Application Load Balancer, Amazon Route 53, Elastic Load Balancer, Global Accelerator. I also not implemented AWS Shield Advanced is I can’t afford the minimal charge leveraging this service for learining purpose. Following I had provided some basic information, if you are implementing AWS Shield Standard or Advanced, following details might be useful for you.

## How AWS Shield is Enabled by Default

1. **Automatic Activation**:
    - AWS Shield Standard is inherently active for supported AWS services as soon as you create and use these services. No setup is required on your part.
    - It continuously monitors network traffic to detect and mitigate DDoS attacks in real time.
2. **Global Presence**:
    - AWS Shield Standard operates across AWS’s global infrastructure, including AWS edge locations and data centers, providing protection at the network and application layers.
3. **Integration with AWS Services**: Shield Standard is directly integrated into the architecture of the following AWS resources:
    - **Amazon CloudFront**: Protects web applications and APIs distributed globally via CloudFront’s edge locations.
    - **Application Load Balancer (ALB)**: Secures applications served through ALB by absorbing malicious traffic.
    - **Amazon Route 53**: Safeguards DNS queries from DDoS attacks like query floods or reflection attacks.
    - **Elastic Load Balancer (ELB)**: Mitigates volumetric and application-layer attacks.
    - **AWS Global Accelerator**: Provides DDoS resilience for TCP and UDP traffic.
4. **No Customer Action Required**:
    - The Shield Standard protections are built into the AWS infrastructure.
    - Customers only need to use the supported AWS services to automatically gain Shield Standard protection.

## What AWS Shield Standard Protects

1. **Volumetric Attacks**:
    - Blocks large-scale floods of traffic designed to overwhelm bandwidth or resources.
2. **State-Exhaustion Attacks**:
    - Protects against attempts to deplete stateful network resources (e.g., firewalls, load balancers).
3. **Application-Layer Attacks**:
    - Mitigates some basic application-level DDoS attacks by integrating with services like AWS WAF (for finer-grained controls).

## Some Instructions for AWS Shield Advanced

Setting up **AWS Shield Advanced** involves enabling it in your AWS account, associating the appropriate resources, configuring protection settings, and monitoring for potential DDoS attacks. Below are detailed step-by-step instructions:

## Step 1: Prerequisites

1. **AWS Account**:
    - Ensure you have an active AWS account.
    - Be aware that AWS Shield Advanced incurs a cost starting at $3,000 per month.
2. **Supported Resources**: AWS Shield Advanced can protect the following resources:
    - Amazon CloudFront distributions
    - Application Load Balancers (ALB)
    - Elastic Load Balancers (ELB)
    - Amazon Route 53 hosted zones
    - AWS Global Accelerator
3. **IAM Permissions**:
    - Ensure your IAM user or role has the necessary permissions to configure Shield Advanced. Add the policy: `AWSShieldFullAccess`.

## Step 2: Enable AWS Shield Advanced

1. **Log in to the AWS Management Console**:
    - Navigate to the [AWS Shield Console](https://console.aws.amazon.com/waf/home#/ddosdashboard).
2. **Activate Shield Advanced**:
    - In the Shield dashboard, click **"Configure Shield Advanced"**.
    - Select the **AWS Region** where your resources are located.
3. **Enable Shield Advanced**:
    - Review the terms and pricing.
    - Check the box to agree to the terms and click **"Enable Shield Advanced"**.

## Step 3: Associate Resources for Protection

1. **Add Protected Resources**:
    - After enabling Shield Advanced, click **"Add resources to protect"**.
    - Select the type of resource (e.g., CloudFront, ALB, ELB, Route 53, Global Accelerator).
    - Choose the specific resource from the list.
    - Click **"Add resource"** to associate it with Shield Advanced.
2. **Repeat for Additional Resources**:
    - Add all the resources you want Shield Advanced to protect.

## Step 4: Configure DDoS Response Team (DRT) Access

1. **Grant DRT Access**:
    - Shield Advanced provides 24/7 access to AWS's DDoS Response Team.
    - In the Shield dashboard, under **"DRT Access"**, click **"Grant DRT Access"**.
    - This allows AWS experts to assist you during a DDoS attack.
2. **Review IAM Permissions**:
    - Ensure DRT has sufficient permissions to access and mitigate attacks on your resources.

## Step 5: Set Up Proactive Engagement (Optional)

1. **Enable Proactive Engagement**:
    - Shield Advanced offers proactive monitoring and assistance during potential DDoS events.
    - Under **"Proactive Engagement"**, enable the service and provide contact details for AWS to reach you during incidents.

## Step 6: Configure Cost Protection

1. **Activate Cost Protection**:
    - Shield Advanced can protect against unexpected costs incurred due to scaling or data transfer during a DDoS attack.
    - Ensure that **cost protection** is enabled for all protected resources.

## Step 7: Monitor and Analyze Traffic

1. **View Attack Metrics**:
    - Access the **Shield Metrics** in the AWS Management Console to monitor real-time traffic patterns.
    - Use **AWS CloudWatch** to set up alarms for unusual traffic spikes.
2. **Enable Logs and Reports**:
    - For CloudFront and ALB resources, enable access logs to capture detailed traffic data.
    - Route logs to Amazon S3 or a monitoring system for analysis.

## Step 8: Create AWS WAF Rules (Optional but Recommended)

1. **Integrate AWS WAF**:
    - Shield Advanced works seamlessly with AWS WAF to block application-layer DDoS attacks.
    - Configure WAF rules to block or allow specific IPs, patterns, or traffic sources.
2. **Test WAF Rules**:
    - Simulate potential attack patterns and monitor how your WAF rules respond.

## Step 9: Test Your Setup

1. **Simulate Traffic**:
    - Use load-testing tools like Apache JMeter or AWS's Distributed Load Testing tool to simulate high traffic and monitor Shield Advanced's response.
2. **Review Logs**:
    - Check CloudWatch and Shield Advanced metrics to confirm that the system is effectively mitigating attacks.

## Step 10: Review and Maintain

1. **Regularly Update Resources**:
    - As you add new AWS resources (e.g., CloudFront distributions or ALBs), ensure they are associated with Shield Advanced.
2. **Conduct Security Reviews**:
    - Periodically review your Shield Advanced setup and WAF rules for improvements.
3. **Monitor Billing**:
    - Keep track of the Shield Advanced charges and ensure they align with your protection strategy.

# Concept 8: Implementing AWS GuardDuty

AWS GuardDuty acts as a **cloud-centric IDS**, leveraging intelligent threat detection mechanisms to secure AWS resources. It provides **continuous monitoring**, uses advanced analytics to identify potential risks, and integrates with AWS services for automated mitigation. This makes it an essential component of a robust cloud security strategy.

To create and simulate the scenario where an AWS GuardDuty detects and reports findings of a malicious machine communicating with a compromised machine, follow these detailed steps:

## Step 1: Set Up AWS Environment

1. **Create an AWS Account**:
    - If you don’t already have an AWS account, sign up at [AWS Signup Page](https://aws.amazon.com/).
2. **Enable GuardDuty**:
    - Navigate to the **GuardDuty** console in the AWS Management Console.
    - Enable GuardDuty for your region.
    - Ensure that all necessary permissions are granted to GuardDuty (AWS-managed policies for GuardDuty service).
3. **Set Up a Virtual Private Cloud (VPC)**:
    - Create a new VPC or use an existing one.
    - Create subnets (we will be using public subnet).
    - Attach an Internet Gateway to the VPC to allow public internet access.

## Step 2: Create the Machines

1. **Launch the Malicious Machine**:
    - Spin up an EC2 instance in the public subnet.
    - Assign a public IP address.
    - Choose a lightweight Linux distribution (e.g., Amazon Linux 2 or Ubuntu) for simplicity.
    - Configure a Security Group to allow all outbound traffic and limit inbound traffic as needed.
    - ssh to your malicious machine and install nmap tool - `sudo apt install curl`
2. **Launch the Compromised Machine**:
    - Agian spin up another EC2 instance in the public
    - Assign a public IP address (depending on the simulation needs).
    - Configure its Security Group to allow traffic from the public IP of the malicious machine.
    - ssh to your machine and install nginx and configure the html page to show your custom message `<h1>This is compromised machine</h1>`

![image.png](images/image%2079.png)

## Step 3: Upload Threat List file

1. **Prepare a Threat List File**:
    - Create a text file (e.g., `threatlist.txt`) containing the public IP of the malicious machine:

```

```

`18.233.160.81`

1. **Host the Threat List File**:
    - Upload the file to an Amazon S3 bucket.
    - Set appropriate permissions to make it accessible by GuardDuty.
2. **Integrate the Threat List with GuardDuty**:
    - Go to the GuardDuty console and navigate to **Lists**.
    - Add a new **Threat List**:
        - Provide the URL of the S3 object containing the threat list in format - `http://blabla`
        - Specify a name for the list and activate it.

![image.png](images/image%2080.png)

## Step 4: Enable GuardDuty and add the Malicious IP to Threat List

- **Sign In**:
    - Log in to your AWS Management Console.
    - Navigate to the **GuardDuty** console ([GuardDuty Console](https://console.aws.amazon.com/guardduty/)).
- **Enable GuardDuty**:
    - If it’s your first time using GuardDuty, click **Get Started**.
    - Click **Enable GuardDuty**.
- **Some Configurations**:
    - Some protections are enabled by default so no need to do anything for them like - VPC Flow Logs, DNS Logs, AWS CloudTrail Logs, Built-In Threat Intelligence and Findings Generation for **Reconnaissance,** **Unauthorized Access** and **Data Exfiltration.**
    - You can manually enable some more protections according to your requirements like - S3 Protection , EKS Runtime Monitoring, Malware Protection, CloudTrail S3 Data Events.
    - Click **Save**.
- **Verify**:
    - You should see GuardDuty enabled in the **Dashboard**.
- **Adding Threat IP List**
    - Go to Threat IP list under settings and click “Add a Threat IP list
    - Give Threat IP list name and Location in the format - `https://s3.amazonaws.com/bucket-name/file.txt`
    - Give the format as Plain Text and click on checkbox.
    - Now check your Threat IP list, go to Actions and click on Activate.

![image.png](images/image%2081.png)

![image.png](images/image%2082.png)

![image.png](images/image%2083.png)

![image.png](images/image%2084.png)

![image.png](images/image%2085.png)

## Step 5: Simulate Communication

1. **Install Tools for Communication**:
    - You had already installed tools like nginx and curl in your compromised machine (web server) as well as malicious machine (hacker’s machine)
2. **Generate Traffic**:
    - If you try to see the finding from GuardDuty Dashboard then you won’t see anything.
    - From the malicious machine, initiate communication to the compromised machine:
        - Example command: `curl http://<IP_of_compromised_machine>`.
    - This simulates an attacker attempting to exfiltrate data or establish a connection.

![image.png](images/image%2086.png)

![image.png](images/image%2087.png)

![image.png](images/image%2088.png)

![image.png](images/image%2089.png)

![image.png](images/image%2090.png)

## Step 6: Observe GuardDuty Findings

1. **Wait for GuardDuty to Detect**:
    - GuardDuty periodically scans logs (VPC Flow Logs, DNS Logs, CloudTrail, etc.).
    - Detection may take a few minutes.
2. **Check Findings**:
    - Navigate to the **Findings** section in the GuardDuty console.
    - Look for a finding that corresponds to the malicious IP trying to communicate with the compromised machine.
    - Findings will include details such as:
        - **Finding type**: Recon:EC2/PortProbeUnprotectedPort or UnauthorizedAccess:EC2/MaliciousIPCaller.
        - **Resource impacted**: Details about the compromised machine.
        - **Threat intel**: Confirmation that the IP matches the threat list.

## Step 7: Cleanup

- Stop and terminate the EC2 instances to avoid unnecessary costs.
- Remove the threat list from the S3 bucket and deactivate it in GuardDuty.
- Disable GuardDuty if not needed further.

# Concept 9: Working with AWS Security Hub

Setting up and implementing **AWS Security Hub** involves enabling the service, configuring its features, integrating it with other AWS services, and using it to monitor and remediate security findings.

In our scenario, we will leverage AWS Security Hub to receive findings from AWS GuardDuty. We will then create an action within Security Hub that sends finding details to Amazon EventBridge. This configuration will utilize Security Hub as the source, with a Lambda function and SNS notifications as targets. The Lambda function will be responsible for stopping compromised servers identified by GuardDuty. Concurrently, SNS notifications will alert subscribers whenever a malicious machine attempts to attack a compromised server.

![image.png](images/image%2091.png)

## 1.Enable AWS Security Hub

AWS Security Hub must be enabled in each AWS Region where you want to centralize security findings.

### **Step 1: Access Security Hub**

1. Sign in to the **AWS Management Console**.
2. Search for **Security Hub** in the AWS Console search bar and select it.

### **Step 2: Enable the Service**

1. Click **"Get Started"**.
2. Select the Regions where you want to enable Security Hub. It is regional, so you need to enable it separately in each desired Region.
3. Enable the **foundational security best practices** and optional **CIS AWS Foundations Benchmark standard** (these perform automated security checks).
4. Confirm by clicking **"Enable Security Hub"**.

## 2.Integrate Security Hub with AWS Services

Security Hub integrates with AWS services and partner tools to aggregate findings. You can choose integratin as per your business requirements. Here I am just providing the steps for integration so that it would be useful for you if you need in future, currently we don’t need integrations.

### **Step 1: Enable AWS Service Integrations**

1. In the Security Hub Console, go to **"Settings"** > **"Integrations"**.
2. Select the AWS services to integrate with Security Hub, such as:
    - **AWS Config**: Monitors compliance with security best practices.
    - **Amazon GuardDuty**: Provides intelligent threat detection.
    - **Amazon Macie**: Monitors S3 data security.
    - **IAM Access Analyzer**: Analyzes access permissions for potential risks.
3. Click **"Enable"** for each service.

### **Step 2: Enable Third-Party Integrations (Optional)**

1. In the same **Integrations** section, browse supported third-party security tools.
2. Configure and enable integrations based on your requirements (e.g., SIEM tools, vulnerability scanners).

## 3.Configure Security Standards

Security Hub provides automated compliance checks using predefined standards.

### **Step 1: View and Enable Security Standards**

1. Navigate to **"Standards"** in the Security Hub Console.
2. Enable standards like:
    - **AWS Foundational Security Best Practices**.
    - **CIS AWS Foundations Benchmark**.
3. Wait for Security Hub to begin assessing your resources against the enabled standards.

### **Step 2: Review Compliance Checks**

1. Click on a standard to view its security controls.
2. Review the compliance status of your resources for each control.

## 4.Set Up Multi-Account Monitoring (Optional)

For multiple AWS accounts, set up a **master-member** relationship to centralize findings.

### **Step 1: Designate a Master Account**

1. In the Security Hub Console, go to **"Settings"** > **"Accounts"**.
2. Click **"Manage accounts"** > **"Add accounts"**.
3. Add member account IDs and send invitations.

### **Step 2: Accept Invitations in Member Accounts**

1. Log in to the member accounts.
2. Navigate to **Security Hub** > **"Settings"** > **“Configuration” > "Accounts"**.
3. Accept the invitation from the master account.

## 5.Monitor and Analyze Security Findings

Security Hub aggregates findings from various integrated services into a standardized format.

### **Step 1: Access Findings**

1. Navigate to **"Findings"** in the Security Hub Console.
2. Use filters to narrow findings by:
    - Severity (Low, Medium, High, or Critical).
    - Resource type (e.g., EC2 instance, S3 bucket).
    - AWS service or third-party tool.

### **Step 2: Review and Understand Findings**

1. Click on individual findings to view details such as:
    - **Affected Resource**: The specific AWS resource related to the finding.
    - **Description**: Explanation of the issue.
    - **Remediation**: Steps to address the finding.
2. Export findings to **Amazon S3** or integrate with a SIEM for deeper analysis.

## 6.Automate Responses to Findings

Use **Amazon EventBridge** to automate responses based on findings.

### **Step 1: Create a Custom Action in AWS Security Hub**

1. **Log in to AWS Management Console** and navigate to **AWS Security Hub**.
2. Go to **Settings** → **Custom actions**.
3. Click **Create custom action**.
    - **Action name**: Provide a name (e.g., `SendFindingToEventBridge`).
    - **Description**: Add a description (e.g., `Send Security Hub findings to EventBridge`).
    - **ID**: This is auto-generated or you can provide a unique identifier.

Once created, this action will be available for use on Security Hub findings.

![image.png](images/image%2092.png)

### **Step 2: Creating a Lambda Function**

1. Go to the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Click **Create function**.
3. Select **Author from scratch**.
    - **Function name**: Enter a descriptive name (e.g., `StopEC2Instance`).
    - **Runtime**: Select Python 3.x (e.g., Python 3.9).
    - **Role**: Select a Role that have the permissions like AmazonEC2FullAccess and CloudWatchFullAccess.
4. Then click on “Create function”

![image.png](images/image%2093.png)

![image.png](images/image%2094.png)

5.Scroll Down and go to Code tab and write the following code

```python
# Import the boto3 library to interact with AWS services
import boto3

# Define the Lambda function handler
def lambda_handler(event, context):   

    # Initialize an EC2 client using boto3 to interact with the EC2 service
    ec2_client = boto3.client('ec2')
    
    
    # Extract the instance ID from the event details
    arn = event['detail']['findings'][0]['Resources'][0]['Id']
    instance_id = arn.split('/')[-1]

    # Stop the EC2 instance using the extracted instance ID
    # The 'stop_instances' method sends a request to stop the specified EC2 instance
    response = ec2_client.stop_instances(InstanceIds=[instance_id])

    
    
    # Return a response indicating the action taken
    # This includes the instance ID and the response from the stop_instances API call
    return {
        'statusCode': 200,  # HTTP status code indicating success
        'body': f"Instance {instance_id} is being stopped. Response: {response}"  # Response body with details
    }
```

![image.png](images/image%2095.png)

### **Step 3: Create an EventBridge Rule**

- Navigate to the **Amazon EventBridge Console**.
- Go to **Rules** → Click **Create rule**.
- **Rule details**:
    - **Name**: Enter a descriptive name (e.g., `SecurityHubFindingRule`).
    - **Description**: Add a description (e.g., `Triggers when Security Hub custom actions are invoked`).
    - **Event bus**: Use the default event bus (`default`).
- **Define a pattern**:
    - Choose **Event pattern** and select **Custom pattern**.
    - Use the following pattern to filter for Security Hub findings related to the custom action:

```python
{
  "source": ["aws.securityhub"],
  "detail-type": ["Security Hub Findings - Custom Action"],
  "detail": {
    "actionName": ["SendFindingToEventBridge"]
  }
}
```

1. **Select targets**:
    - Add a target for the rule. For example:
        - **Lambda function**: To process the finding, attach the Lambda function `StopEC2Instance`
        - **SNS Topic**: To notify administrators create an SNS Topic and add subscribers to it. Then Add that SNS topic as target.
    - Configure the target settings as needed.
2. **Create the rule**:
    - Click on Next then Agin Next
    - Review the rule and click **Create rule**.

![image.png](images/image%2096.png)

![image.png](images/image%2097.png)

![image.png](images/image%2098.png)

![image.png](images/image%2099.png)

![image.png](images/image%20100.png)

### **Step 4: Test the Integration**

1. Go to **Security Hub** and find a security finding.
2. Select the finding and click **Actions** → **Custom action**.
3. Choose the custom action (`SendFindingToEventBridge`) you created earlier.
4. Verify that the rule in EventBridge is triggered by checking:
    - **CloudWatch Logs**: If you set a logging target.
    - **Target service**: (e.g., Lambda, SQS) for received data.
    - Check whether your instance is terminated or not

![image.png](images/image%20101.png)

![image.png](images/image%20102.png)

# Concept 10: Implementing TLS Termination (AWS ACM)

## Approach 1: Implementing TLS Termination to a website hosted on s3

## Step 1: Requesting a certificate from AWS Certificate Manager

1. Go to the AWS Certificate Manager service and select the 'US East (N. Virginia)' region. This region acts as a central hub for distributing certificates for CloudFront distributions.
2. Request a certificate. When prompted for the certification type, select "Request a public certificate" and then click "Next." On the next page, when asked for Domain Names, provide the fully qualified domain names, meaning a list of subdomains along with the root domain. Keep all other settings at their default values and click the "Request" button.

![image.png](images/image%20103.png)

1. On the next screen, you will see the certificate state as "pending." Copy the "Record Name" and "Value" and paste them into the DNS Record Set database of your DNS provider. Soon, the status of your certificate will change to "verified.”

![image.png](images/image%20104.png)

1. If you've followed all the steps correctly and the certificate validation is still pending in AWS Certificate Manager, consider creating a hosted zone in Route 53. Replace the existing nameservers with those provided by Route 53. This will allow you to manage all DNS records, including those required for certificate validation, within Route 53.

## Step 2: Hosting website in S3

- Create an S3 bucket with ACL enabled and public access enabled. Then upload your index.html to the bucket.
- Set the bucket policy such that all the objects of bucket becomes public

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

## Step 3: Add Domain to Cloudfront

1. To configure your CloudFront distribution, navigate to the distribution and click "Edit" to access its settings. In the "Alternate Domain Names" section, enter the list of domains (including subdomains) that you want to associate with your website. Select the custom SSL certificate that you created in the N. Virginia region of AWS Certificate Manager. Finally, click "Save Changes" to apply your configurations.

![image.png](images/image%20105.png)

![image.png](images/image%20106.png)

1. Now, add CNAME records to your DNS dashboard or hosted zone. Set the "Name" of each record to the corresponding subdomain, and set the "Value" to the distribution domain name obtained from your CloudFront distribution.

![image.png](images/image%20107.png)

Please allow some time for the domain name provider to update its name servers with the changes you've made.

## Approach 2: Implementing TLS Termination to a website hosted on EC2

## Step 1: Requesting a certificate from AWS Certificate Manager

1. Go to the AWS Certificate Manager service and select the 'US East (N. Virginia)' region. This region acts as a central hub for distributing certificates for CloudFront distributions.
2. Request a certificate. When prompted for the certification type, select "Request a public certificate" and then click "Next." On the next page, when asked for Domain Names, provide the fully qualified domain names, meaning a list of subdomains along with the root domain. Keep all other settings at their default values and3click the "Request" button.

![image.png](images/image%20108.png)

1. On the next screen, you will see the certificate state as "pending." Copy the "Record Name" and "Value" and paste them into the DNS Record Set database of your DNS provider. Soon, the status of your certificate will change to "verified.”

![image.png](images/image%20109.png)

1. If you've followed all the steps correctly and the certificate validation is still pending in AWS Certificate Manager, consider creating a hosted zone in Route 53. Replace the existing nameservers with those provided by Route 53. This will allow you to manage all DNS records, including those required for certificate validation, within Route 53.

## Step 2: Hosting Website on EC2 instance

1. Just host your website in your EC2 instance. Ensure website is accessible through the public ip address with port 80 (http) to your server.
2. Here for demo pupose I had installed nginx and add a text to index.html i.e. “**This is shobhit's website” .**
3. Then I had tried to access the website using public ip with port 80 (http).

![image.png](images/image%20110.png)

## Step 3: Set up Application Load Balancer

1. First Create a Target Group which points your EC2 instance with port 80 and http protocol.
2. Register your EC2 instance as a target.
3. Then Create an Application Load Balancer and which should be of internet facing

![image.png](images/image%20111.png)

1. Add your VPC, Availability Zones (atleast 2 AZ) and subnets (atleast 2 public subnets are required) where your EC2 instance resides.
2. Set the security group which having a rule of http and https enabled (and other if required ).
3. **Configure Listener**
    - Set the https protocol and your Target group which you had just created.
    - Scroll down to Secure Listening Section and select certificate source from ACM. Then select your SSL certificate.
    - Then click on Create Load Balancer

![image.png](images/image%20112.png)

![image.png](images/image%20113.png)

![image.png](images/image%20114.png)

## Step 4: Copy DNS name to the Record Set

1. Again Navigate to your Load balancer Dashboard then click your Load Balancer.
2. Copy the DNS Name of your Load Balancer and paste it as CNAME to Record Set of DNS Provider.
3. Keep in mind to set the name as your Custome domain name for your website. In my case, in CNAME Record, I put Record Name as `test.itshobhit.co.in` and Record Value as `myALB-1773698765.us-east-1.elb.amazonaws.com` . Then Save it
4. At last type your domain name to Address bar and get your website with SSL certification.

![image.png](images/image%20115.png)

![image.png](images/image%20116.png)

# Concept 11: Enable logging via AWS CloudTrail

To enable AWS CloudTrail logging so that events are stored in both an S3 bucket and CloudWatch log groups, follow these detailed steps:

## Step 1: Create a CloudTrail and Send Logs to S3

1. **Go to the CloudTrail Console**:
    - Navigate to the [AWS CloudTrail Console](https://console.aws.amazon.com/cloudtrail/).
2. **Create a Trail**:
    - Click **"Create trail"**.
3. **Trail Details**:
    - Enter a name for the trail (e.g., `MyCloudTrail`).
4. **Select Storage Location**:
    - **S3 Bucket**: Create a new one or select the bucket you created earlier (in case you are using already created bucket then you need to update the bucket permission so that cloudtrail can perform write operation on it.
    - Enable log file encryption using AWS KMS if required. I had disabled them as I don’t need them.
5. **Enable CloudWatch Logs**
    - Enable the CloudWatch Logs, provide a new log group name and give a new IAM Role name.
    - Then click “Next”
6. **Choose log events**:
    - You can select type of Events you want to record through cloudtrail.
    - Accoring to requirements you can choose Management events, Data events, insights events and Network activity events.
    - I had just choosed only Management Events and then keep all the remaining things default.
    - Then click on Next.
7. **Review and Create:**
    - Review all the details, if you feel everything okay, then click on create trial.

![image.png](images/image%20117.png)

![image.png](images/image%20118.png)

![image.png](images/image%20119.png)

![image.png](images/image%20120.png)

![image.png](images/image%20121.png)

## Step 2: Test and Verify Logging

1. **Trigger Events**:
    - Perform actions in your AWS account, such as creating an EC2 instance or modifying an S3 bucket policy.
2. **Check S3 Bucket**:
    - Navigate to your S3 bucket and look for a folder named `AWSLogs/<account-id>/CloudTrail/`. Logs will be stored in a time-stamped structure.
3. **Check CloudWatch Logs**:
    - Navigate to the [CloudWatch Logs Console](https://console.aws.amazon.com/cloudwatch/home#logs).
    - Select your log group and verify that CloudTrail logs are being delivered.

![image.png](images/image%20122.png)

![image.png](images/image%20123.png)

![image.png](images/image%20124.png)

# Concept 12: Managing Secrets using AWS Secret Manager

## Step 1: Create a IAM Role

1. Go to IAM dashboard and navigate to Roles section then click “Create role”.
2. Select Trusted Entity type as AWS Service and use case as EC2. Then attach Permission Policy `SecretsManagerReadWrite` . Then click on “Next”.
3. Give any Desired name. I gave “role_secret_manager”. Then click on bottom right corner “Create role”.

## Step 2: Set up your machine

- Make sure your EC2 instance is running where you want to fetch the secrets. I am using Ubuntu 24.04.
- Install AWS CLI from official website -
1. [Installing or updating to the latest version of the AWS CLI - AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) . Also make sure that proper json parser (like jq) is also installed in your machine.
2. Now we are going to attach a role to EC2 instance which we had created just above, for that, go to EC2 dashboard and check your machine. Then click “Actions” and go to “Security” section. Click “Modify IAM Role”. Open dropdown, choose your IAM Role. I had chosen `role_secret_manager` in my case. Then click “update IAM Role”

## Step 3: Creating Secrets in Secret Manager

1. Go to Secret Manager Dashboard and click “Store a new secret”. Choose secret type as “Other type of secret”.
2. Give the items of secrets in the form of key and value form interface. There's no explicit limit on the number of key-value pairs, but the total size of the secret (including all keys and values) must stay within the 64 KB size limit.
3. Then click on “Next”.
4. Give appropriate secret name. I gave “test-secrets-01” . Give description if you want. Leave all the remaining fields as it is. Scroll to bottom and click on “Next”.
5. Again click “Next” and Review all the details. After ensuring, everything is correct, click “Store” at the bottom.
6. Then you will see that your secrets made successfully on secret manager.

![image.png](images/image%20125.png)

![image.png](images/image%20126.png)

![image.png](images/image%20127.png)

## Step 4: Fetching the secret

1. SSH to your EC2 instance and go to directory where you want to fetch the secret.
2. Write the following bash script at the same directory

```bash
#!/bin/bash

# Define variables
SECRET_ID="$1"          # Secret ID passed as the first argument
OUTPUT_FILE="$2" # Output file to store the key-value pairs

# Check if SECRET_ID and new file name is provided
if [[ -z "$SECRET_ID" && -z "$OUTPUT_FILE" ]]; then
  echo "Usage: $0 <secret-id>"
  exit 1
fi

# Fetch the secret value using AWS CLI
SECRET_JSON=$(aws secretsmanager get-secret-value --secret-id "$SECRET_ID" --query 'SecretString' --output text 2>/dev/null)

# Check if the command succeeded
if [[ $? -ne 0 || -z "$SECRET_JSON" ]]; then
  echo "Failed to retrieve the secret. Please check the secret ID and your AWS credentials."
  exit 1
fi

# Parse the JSON object and write key-value pairs to the output file
echo "Writing secret data to $OUTPUT_FILE..."
echo "$SECRET_JSON" | jq -r 'to_entries | .[] | "\\(.key)=\\(.value)"' > "$OUTPUT_FILE"

# Verify the file creation
if [[ $? -eq 0 ]]; then
  echo "Secret data successfully written to $OUTPUT_FILE."
else
  echo "Failed to write secret data to $OUTPUT_FILE."
  exit 1
fi

```

1. Run the bash script by using command and also provide the secret id as argument `bash reterive-secrets.sh <your-secret-id> <your-output-file>`

![image.png](images/image%20128.png)

# Concept 13: Enabling Encryption using AWS KMS

Leaving file unencrypted is not a good practice. We need to impose encryption in order to make secret protected. We can use tool like **OpenSSL** for encrypting and decrypting files locally. AWS KMS service also provides same feature of encryption and decryption.

We are going to see that how we can perform encryption and decryption in the file present in EC2 instance. Then we will see how we can perform encryption to other AWS Services.

## Encryption and decryption in the file present in EC2 instance

## Step 1: Creating a Key in AWS KMS

1. **Create an IAM Role for KMS Service**
    1. Go to IAM dashboard, create a new role, Select trusted entity as AWS Service, give use case as KMS. Click “Next”.
    2. You will see a policy `AWSKeyManagementServiceCustomKeyStoresServiceRolePolicy` is already assigned. No need to do anything, click Next.
    3. Again you will see that Role name is already assigned as `AWSServiceRoleForKeyManagementServiceCustomKeyStores` . No need to do anything. Scroll and click “Create Role”
2. Now go to the AWS Management Console and navigate to KMS (Key Management Service) from the Services menu.
3. In the KMS console, click on Create key.
4. Give the key configuration as key type (symmetric/Asymmetric) and key usage as encypt and decrypt.
    - **Symmetric** (for most use cases like encryption/decryption).
    - **Asymmetric** (for use with digital signing and verification).
5. Give the key alias (e.g., `MyEncryptionKey`) and description (optional).
6. This blog can be useful - [https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html#key-policy-default-allow-administrators](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html#key-policy-default-allow-administrators)
7. When it ask to “Define key administrative permissions” just select `AWSServiceRoleForKeyManagementServiceCustomKeyStores` click “Next”.
8. When it ask to “Define key usage permissions” again select `AWSServiceRoleForKeyManagementServiceCustomKeyStores` click “Next”.
9. Review the changes and click “Finish”

![image.png](images/image%20129.png)

![image.png](images/image%20130.png)

![image.png](images/image%20131.png)

## Step 2: Make machine ready

- **Get your Secret file:**
    1. Just review the section “Managing Secrets using AWS Secret Manager” where we had created a secret file. By following those steps, we will be able to get generate a secret file in our system. If you already have a secret file present in your current directory then igonre this point.
- **Provide permission to use KMS service:**
    1. Apart from secret file, we need additional permission to use KMS service to our EC2 instance. So you must create a policy.
    2. For Creating a policy, go to IAM dashboard, go to policy section, click “create policy. Select service “KMS” . Then select JSON Editor and write the following policy. Then click “Next”.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:GenerateDataKey",
                "kms:DescribeKey",
                "kms:CreateAlias",
                "kms:CreateKey",
                "kms:DeleteAlias",
                "kms:Describe*",
                "kms:GenerateRandom",
                "kms:Get*",
                "kms:List*",
                "kms:TagResource",
                "kms:UntagResource",
                "iam:ListGroups",
                "iam:ListRoles",
                "iam:ListUsers"
            ],
            "Resource": [
                "arn:aws:kms:<YOUR_AWS_REGION>:<YOUR_AWS_ACCOUNT_ID>:key/<YOUR_KMS_KEY_ARN>" 
            ]
        }
    ]
}

```

- Give Policy name as per your choice (eg `KMSPolicy` ). Description if you want. Then click create policy.
- Now creating a new role, go to roles, click “create role”. Select trusted entity as AWS Service, give use case as EC2. Click “Next”.
- Give Role name as `EC2_encryption_decryption_role` and give the policy as `KMSPolicy` (created just above) and scroll down. Then click on create role.
- Now we are going to provide this role `EC2_encryption_decryption_role` to your instance. Just select the instance form EC2 instance dashboard. Go to actions and then go to security section. Now click “Modify IAM Role”.
- Choose your role `EC2_encryption_decryption_role` and click on update IAM Role.

![image.png](images/image%20132.png)

![image.png](images/image%20133.png)

![image.png](images/image%20134.png)

1. **Providing KMS Key ID to system:** Providing KMS is crucial as it imposes all the security to our secret. Leakage of KMS Key ID shows mismanagement of secrets. Hence storing the KMS Key ID in environment variable is the best option instead of hard coding into the script.
    1. SSH to your EC2 instance .
    2. Add the following line using nano editory (`nano /root/.bashrc and nano ~/.bashrc`) `export AWS_KMS_KEY_ID=”<your-kms-key-id>`
    3. Source your files `source /root/.bashrc source ~/.bashrc`

## Step 3: Encrypting your file

1. Go to the directory where you have source file (secret file) which you want to encrypt.
2. Write the following bash script ( `encrypt.sh` )that encypt the secret using AWS KMS

```bash
#!/bin/bash

# Check if the correct number of arguments are passed
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <file-to-encrypt> <encrypted-file>"
  exit 1
fi

# Define the input and output file names
INPUT_FILE="$1"      # File to encrypt
OUTPUT_FILE="$2"     # Encrypted file to store the result

# Check if the input file exists
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File '$INPUT_FILE' does not exist."
  exit 1
fi

# Define the KMS Key ID 
KMS_KEY_ID=$AWS_KMS_KEY_ID  # We are providing key ID using environment variable

# Encrypt the file using AWS KMS
aws kms encrypt \\
    --key-id "$KMS_KEY_ID" \\
    --plaintext fileb://"$INPUT_FILE" \\
    --output text \\
    --query CiphertextBlob \\
    | base64 --decode > "$OUTPUT_FILE"

# Check if the encryption was successful
if [ $? -eq 0 ]; then
  echo "File '$INPUT_FILE' has been successfully encrypted and saved to '$OUTPUT_FILE'."
else
  echo "Error: Encryption failed."
  exit 1
fi

```

1. For using above script, use this format - `sh encrypt.sh <file-to-encrypt> <encrypted-file>`

## Step 4: Decrypting file

1. We had all the set up ready, what we need is to decrypt the same flle which we had just encyrpted.
2. Create a bash script with the name `decrypt.sh`

```bash
#!/bin/bash

# Check if the correct number of arguments are passed
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <encrypted-file> <decrypted-file>"
  exit 1
fi

# Define the input and output file names
ENCRYPTED_FILE="$1"   # File that was encrypted
DECRYPTED_FILE="$2"   # File to store the decrypted content

# Check if the encrypted file exists
if [ ! -f "$ENCRYPTED_FILE" ]; then
  echo "Error: File '$ENCRYPTED_FILE' does not exist."
  exit 1
fi

# Decrypt the file using AWS KMS
aws kms decrypt \\
    --ciphertext-blob fileb://"$ENCRYPTED_FILE" \\
    --output text \\
    --query Plaintext \\
    | base64 --decode > "$DECRYPTED_FILE"

# Check if the decryption was successful
if [ $? -eq 0 ]; then
  echo "File '$ENCRYPTED_FILE' has been successfully decrypted and saved to '$DECRYPTED_FILE'."
else
  echo "Error: Decryption failed."
  exit 1
fi

```

1. For running the bash script, use code - `sh decrypt.sh <encrypted-file> <decrypted-file>`
2. Then you will got your decrypted file, use it as per your application requirement.

## Encrypting Other AWS Services

AWS Key Management Service (KMS) integrates with numerous AWS services to provide encryption for sensitive data. Here’s a comprehensive list of AWS services where you can implement encryption using AWS KMS:

### **1. Compute**

- **Amazon EC2**:
    - Encrypt data stored in EBS volumes, snapshots, and AMIs.
- **AWS Lambda**:
    - Encrypt environment variables and secrets using KMS.
- **Amazon Lightsail**:
    - Encrypt attached block storage disks using KMS.

### **2. Storage**

- **Amazon S3**:
    - Encrypt objects using S3-KMS server-side encryption (SSE-KMS).
    - Encrypt bucket policies or inventory reports.
- **Amazon EFS (Elastic File System)**:
    - Enable encryption for file systems and access logs.
- **Amazon FSx**:
    - Encrypt file systems for Windows File Server and Lustre.

### **3. Databases**

- **Amazon RDS**:
    - Encrypt RDS databases, snapshots, and read replicas.
- **Amazon Aurora**:
    - Encrypt Aurora clusters, backups, and logs.
- **Amazon DynamoDB**:
    - Encrypt table data with KMS-managed keys.
- **Amazon ElastiCache**:
    - Encrypt Redis or Memcached clusters.
- **Amazon Redshift**:
    - Encrypt Redshift clusters and snapshots.

### **4. Messaging and Queues**

- **Amazon SQS**:
    - Encrypt messages in standard or FIFO queues.
- **Amazon SNS**:
    - Encrypt messages sent to topics.
- **Amazon MQ**:
    - Encrypt ActiveMQ or RabbitMQ brokers.

### **5. Analytics**

- **Amazon EMR (Elastic MapReduce)**:
    - Encrypt logs, data stored on HDFS, and data in transit.
- **Amazon Athena**:
    - Encrypt query results written to S3.
- **Amazon Kinesis**:
    - Encrypt data streams with KMS.
- **AWS Glue**:
    - Encrypt ETL jobs and metadata.

### **6. Networking**

- **Amazon VPC**:
    - Encrypt VPC Traffic Mirroring data stored in S3.
- **AWS Global Accelerator**:
    - Encrypt accelerator data logs.

### **7. Developer Tools**

- **AWS CodePipeline**:
    - Encrypt pipeline artifacts.
- **AWS CodeBuild**:
    - Encrypt build artifacts and logs.
- **AWS CodeDeploy**:
    - Encrypt deployment configuration files.

### **8. Management and Governance**

- **AWS CloudTrail**:
    - Encrypt logs stored in S3.
- **AWS Config**:
    - Encrypt configuration snapshots.
- **AWS Systems Manager Parameter Store**:
    - Encrypt sensitive parameters (e.g., API keys, passwords).
- **AWS Backup**:
    - Encrypt backup data for supported AWS resources.

### **9. Security and Identity**

- **AWS Secrets Manager**:
    - Encrypt secrets stored in the service.
- **AWS Certificate Manager (ACM)**:
    - Securely manage private certificates using KMS.

### **10. Machine Learning**

- **Amazon SageMaker**:
    - Encrypt notebook instances, training jobs, and endpoints.
- **Amazon Comprehend**:
    - Encrypt processed data and results.
- **Amazon Rekognition**:
    - Encrypt image data and metadata.

### **11. Edge Services**

- **Amazon CloudFront**:
    - Encrypt logs stored in S3 using SSE-KMS.
- **AWS IoT Core**:
    - Encrypt device data and messages.

### **12. Backup and Archival**

- **Amazon S3 Glacier**:
    - Encrypt archival data with KMS.
- **AWS Backup**:
    - Encrypt backups created for AWS services like RDS, DynamoDB, and EFS.

# Concept 14: Enabling Automatic Backup Amazon Data Lifecycle Manager (DLM)

## Steps to Setting up and managing backups

1. Go to the [Amazon EC2 Console](https://console.aws.amazon.com/ec2/).
2. In the left-hand navigation pane, under **Elastic Block Store**, select **Lifecycle Manager**.
3. **Click on "Create lifecycle policy".**
4. When it ask whether to use a custom or default policy, choose “Custom Policy”.
5. **In the section “Schedule-based policy”** choose any one option as per your requrement
    1. EBS Snapshot policy : Create a policy that automates the creation, retention, and deletion of EBS snapshots.
    2. EBS Backed AMI policy : Create a policy that automates the creation, retention, and deletion of EBS-backed AMIs.
6. In the section “Target Resources”, select your target resource type:
    1. **Volume** : This option targets **EBS volumes** directly. It creates **snapshots** of the specified EBS volumes based on the policy's schedule.
    2. **Instance** : This option targets **EC2 instances**. It creates **Amazon Machine Images (AMIs)** of the instances, which include root volume and Metadata about the instance, such as its configuration and attached block devices.
7. Then give Name and value to the resource.
8. Scroll Down to bottom. Give Policy status as Enabled.
9. Giving Schedule details
    1. Schedule name : A descriptive name for the schedule. It helps you identify the specific backup schedule within the lifecycle policy.
    2. Frequency : The time interval at which the backups are created. Options include hourly, daily, weekly, or custom time periods.
    3. Every : Works in conjunction with **Frequency** to specify the exact interval for backups. For eg if **Frequency** is "Daily" and **Every** is "2," backups will occur every 2 days.
    4. Starting at : The time when the first backup will be created. Time is specified in **UTC**.
    5. Retention type : Specifies how long the backups will be retained. Options include: **Count-Based**: Retain a specific number of backups (e.g., keep the last 5 snapshots). **Age-Based**: Retain backups for a specific time period (e.g., retain backups for 7 days or 1 year).
    6. Keep : Works with **Retention Type** to define the number of backups to retain or the time period for retention. For eg if **Retention Type** is "Count-Based" and **Keep** is "5," only the last 5 backups are retained. If **Retention Type** is "Age-Based" and **Keep** is "7 days," backups older than 7 days are automatically deleted.

![image.png](images/image%20135.png)

![image.png](images/image%20136.png)

![image.png](images/image%20137.png)

1. Now let’s test the policy. For testing it, you can check the snapshots and AMI’s . This lifecycle policy would make regular backups for your.

# Concept 15: Setting up Alerts using AWS CloudWatch and SNS

Setting up alerts using **Amazon CloudWatch** and **Amazon SNS** involves monitoring a metric, setting a threshold, and notifying users when the threshold is breached. Here's a step-by-step guide:

## Step 1: Set Up an SNS Topic for Notifications

1. **Go to the SNS Console**:
    - Open the [Amazon SNS Console](https://console.aws.amazon.com/sns).
2. **Create a New Topic**:
    - Click **Topics** in the left-hand menu and then **Create topic**.
    - Choose the type of topic:
        - Standard (default) for most use cases.
    - Provide a **Name** (e.g., `CloudWatchAlertTopic`).
    - Click **Create topic**.
3. **Add Subscriptions**:
    - After creating the topic, select it and click **Create subscription**.
    - Choose the **Protocol** (e.g., `Email` or `SMS`).
    - Enter the **Endpoint** (e.g., your email address or phone number).
    - Click **Create subscription**.
    - Confirm the subscription (e.g., via email).

![image.png](images/image%20138.png)

![image.png](images/image%20139.png)

![image.png](images/image%20140.png)

![image.png](images/image%20141.png)

![image.png](images/image%20142.png)

## Step 2: Identify the Metric to Monitor in CloudWatch

1. **Go to the CloudWatch Console**:
    - Open the [Amazon CloudWatch Console](https://console.aws.amazon.com/cloudwatch).
2. **Navigate to Metrics**:
    - In the left-hand menu, click **Metrics**.
    - Choose a namespace and metric to monitor (e.g., `EC2` metrics like `CPUUtilization`, or custom metrics).
3. **Select the Metric**:
    - Use the filters to locate the specific metric you want to monitor.
    - Click on the metric to view its graph and details.

![image.png](images/image%20143.png)

![image.png](images/image%20144.png)

![image.png](images/image%20145.png)

## Step 3: Create a CloudWatch Alarm

1. **Go to Alarms**:
    - In the CloudWatch Console, click **Alarms** in the left-hand menu.
    - Click **Create alarm**.
2. **Select the Metric**:
    - Click **Select metric** and choose the metric you identified in Step 2.
    - Click **Select metric** to proceed.
3. **Set the Threshold**:
    - Define the conditions for the alarm:
        - **Threshold type**: Static or Anomaly detection.
        - **Condition**: For example, "Greater than 80% for CPUUtilization."
        - **Datapoints**: Specify the number of evaluation periods before triggering the alarm.
4. **Configure Actions**:
    - Under **Notification**, click **Add notification**.
    - Choose the SNS topic you created earlier (e.g., `CloudWatchAlertTopic`).
    - Set separate actions for alarm states like `OK`
    - Then scroll to bottom and click “Next”
5. **Name the Alarm**:
    - Provide a descriptive name for the alarm (e.g., `HighCPUUtilizationAlarm`).
6. **Review and Create**:
    - Review the configuration.
    - Click **Create alarm**.

![image.png](images/image%20146.png)

![image.png](images/image%20147.png)

![image.png](images/image%20148.png)

![image.png](images/image%20149.png)

![image.png](images/image%20150.png)

![image.png](images/image%20151.png)

## Step 4: Test the Alert

1. **Simulate a Trigger**:
    - SSH to your EC2 instance, install the package by `sudo apt install stress-ng`
    - Increase the CPU utilization by command `stress-ng --cpu 4 --cpu-load 75 --timeout 60`
    - Monitor your machine performance in another terminal window by using command `htop`
2. **Check SNS Notifications**:
    - Verify that the SNS notification is delivered to the configured endpoint (e.g., your email or phone).

![image.png](images/image%20152.png)

![image.png](images/image%20153.png)

## Step 5: Monitor and Manage

1. **View Alarm Status**:
    - Go to the **CloudWatch Alarms** section to monitor alarm status (e.g., `OK`, `ALARM`, or `INSUFFICIENT_DATA`).
2. **Update as Needed**:
    - Modify the alarm or SNS configuration if required, such as adding more subscribers.

![image.png](images/image%20154.png)

# Concept 16: Managing Resource access Permissions using IAM Roles

Managing resource permissions in AWS using policies for users and roles involves defining and applying **IAM policies** to control access to resources. Below is a comprehensive guide on how to manage permissions effectively.

### **Key Concepts**

1. **IAM Policies**: JSON documents that define permissions.
    - **Managed Policies**: Predefined by AWS or created by you.
    - **Inline Policies**: Embedded directly in a user, group, or role.
2. **Users**: Individual identities used for human access.
3. **Roles**: Intended for workloads (applications, EC2 instances, etc.) to assume for temporary access.
4. **Principals**: Users or roles that the policy applies to.

## Procedure

We had already running an EC2 instance and AWS CLI is already installed. What we are going to do is, we will creating a IAM Role which would have a policy which represents permission to list all s3 buckets. Then we will assign this role to EC2 instance and check wheter permission are working or not.

## Step 1: **Write an IAM Policy**

IAM policies are JSON documents. Here’s an example structure:

**Example: Allow S3 Read-Only Access**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "*"
        }
    ]
}

```

**Components Explained**:

- `Effect`: Determines whether to **Allow** or **Deny** access.
- `Action`: Specifies the API actions (e.g., `s3:GetObject`).
- `Resource`: Specifies the AWS resources (e.g., an S3 bucket).
- `Condition` (optional): Adds further granularity (e.g., IP restrictions).

You can attach policies to:

- **Users**: For direct access by individuals.
- **Groups**: To manage permissions for multiple users.
- **Roles**: For granting permissions to AWS services or applications.

Follow given instructions to create a policy.

1. Using the AWS Management Console go to the IAM service and click Policies in the left navigation pane and then from top right corner click Create Policy.
2. Choose the JSON tab and paste your policy JSON that you had seen just above. Then click Next.
3. Give Policy name (e.g. S3BucketListingPolicy) , give description and follow the prompts
4. Then review all the details, scroll down and click “Create Policy” at bottom right corner.

![image.png](images/image%20155.png)

![image.png](images/image%20156.png)

![image.png](images/image%20157.png)

![image.png](images/image%20158.png)

![image.png](images/image%20159.png)

![image.png](images/image%20160.png)

## Step 2: Creating Role and Attaching Policy

1. Sign in to the AWS Management Console and navigate to the **IAM** service. Then In the left-hand navigation pane, click on **Roles** and click the **Create Role** button on top right corner.
2. Select the trusted entity type as AWS service, use case as EC2 and click **Next**.
3. On the **Attach permissions policies** page select the policy that you had made.
4. Provide a Role Name (e.g., CustomPolicyRole) and a Description. Optionally, add tags for easier identification if you wish.
5. At last review the role details, then click Create Role.

![image.png](images/image%20161.png)

![image.png](images/image%20162.png)

![image.png](images/image%20163.png)

![image.png](images/image%20164.png)

![image.png](images/image%20165.png)

![image.png](images/image%20166.png)

## Step 3: Apply Roles to Application

- **Use Cases**:
    - EC2 instance access.
    - Lambda function execution permissions.
1. **Go to the EC2 Console**:
    - Navigate to [EC2 Console](https://console.aws.amazon.com/ec2/).
2. **Select the Instance**:
    - Find the instance you want to modify.
    - Select the instance and click **Actions** → **Security** → **Modify IAM role**.
3. **Attach the Role**:
    - In the **Modify IAM role** dialog, select the IAM role you created earlier.
    - Click **Update IAM role**.

![image.png](images/image%20167.png)

## Step 4: Test Access to AWS Resources

To verify that the EC2 instance can access AWS resources:

- Install the AWS CLI if not already installed:

```bash
sudo apt update
sudo apt install unzip
curl "<https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip>" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

- Run an AWS CLI command that requires the permissions granted by the IAM role. For example:

```bash
aws s3 ls
```

Following picture shows listing bucket before assigning IAM Role to EC2 instance

![image.png](images/image%20168.png)

Following picture shows we have been successful to list all s3 buckets after attaching our S3BucketListPolicy to our EC2 instance.

![image.png](images/image%20169.png)

# Conclusion

By implementing these measures, your AWS environment is equipped with a multi-layered security framework that ensures data confidentiality, integrity, and availability. This architecture effectively mitigates risks, adheres to compliance standards, and enhances operational efficiency, enabling your applications to run securely and reliably in the cloud.