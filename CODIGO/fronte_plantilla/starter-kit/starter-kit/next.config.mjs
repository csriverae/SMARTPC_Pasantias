/** @type {import('next').NextConfig} */
const nextConfig = {
    basePath: process.env.BASEPATH,
    experimental: {
        optimizePackageImports: ['@mui/material', '@emotion/react', '@emotion/styled', 'classnames']
    },
    redirects: async () => {
        return [
            {
                source: '/',
                destination: '/login',
                permanent: true,
                locale: false
            }
        ];
    }
};

export default nextConfig;
