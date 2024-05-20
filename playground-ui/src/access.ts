export default function access(initialState: any) {
    const { userId } = initialState || {};

    return {
        canLogin: userId?.userName
    };
}
